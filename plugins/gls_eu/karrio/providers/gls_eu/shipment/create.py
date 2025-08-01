"""Karrio GLS EU shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.error as error
import karrio.providers.gls_eu.units as provider_units
# CRITICAL: Always import and use the generated schema types
import karrio.schemas.gls_eu.shipment_request as gls_req
import karrio.schemas.gls_eu.shipment_response as gls_res


def parse_shipment_response(
    _response: lib.Deserializable,
    settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Convert to typed object using generated schema
    shipment_response = lib.to_object(gls_res.ShipmentResponseType, response)
    
    shipment = None
    if shipment_response:
        shipment = _extract_details(lib.to_dict(shipment_response), settings, _response.ctx)

    return shipment, messages


def _extract_details(
    data: dict,
    settings,
    ctx: dict,
) -> models.ShipmentDetails:
    """Extract shipment details from GLS EU response data"""

    tracking_number = data.get("trackingNumber") or data.get("parcelNumber") or data.get("id")
    shipment_id = str(data.get("shipmentId") or data.get("id") or "")
    
    # Extract label information
    label_url = data.get("labelUrl") or data.get("label", {}).get("url")
    label_content = None
    label_type = "PDF"
    
    if label_url and ctx.get("trace"):
        try:
            label_response = lib.request(url=label_url, trace=ctx["trace"])
            label_content = label_response.body
        except Exception:
            pass  # Label download failed, but shipment creation succeeded

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        docs=models.Documents(
            label=label_content,
        ),
        meta=dict(
            shipment_id=shipment_id,
            label_url=label_url,
            label_type=label_type,
            service_name="GLS EU",
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings,
) -> lib.Serializable:
    """Create a shipment request for the GLS EU API"""

    # Convert karrio models to GLS EU-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
    )

    # Create the GLS EU-specific request object using generated types
    # This is a basic structure - would need to be adapted to actual GLS EU API
    address_from = gls_req.OrderAddress(
        street=shipper.address_line1,
        city=shipper.city,
        state=shipper.state_code or "",
        zipCode=shipper.postal_code,
        country=shipper.country_code,
        apartment=shipper.address_line2,
    )

    address_to = gls_req.OrderAddress(
        street=recipient.address_line1,
        city=recipient.city,
        state=recipient.state_code or "",
        zipCode=recipient.postal_code,
        country=recipient.country_code,
        apartment=recipient.address_line2,
    )

    # Create a basic shipment request object
    # Note: This would need to be adapted to match the actual GLS EU API specification
    request_data = {
        "sender": address_from,
        "recipient": address_to,
        "service": payload.service or "gls_eu_business_parcel",
        "reference": payload.reference or "",
        "packages": [
            {
                "weight": package.weight.value,
                "dimensions": {
                    "length": package.length.value,
                    "width": package.width.value,
                    "height": package.height.value,
                }
            }
            for package in packages
        ]
    }

    # Add options if provided
    if options.gls_eu_cash_on_delivery.state:
        request_data["cash_on_delivery"] = options.gls_eu_cash_on_delivery.state

    if options.gls_eu_insurance.state:
        request_data["insurance"] = options.gls_eu_insurance.state

    if options.gls_eu_saturday_delivery.state:
        request_data["saturday_delivery"] = options.gls_eu_saturday_delivery.state

    return lib.Serializable(request_data, lib.to_dict)
