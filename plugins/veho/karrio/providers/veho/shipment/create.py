"""Karrio Veho shipment API implementation."""

import karrio.schemas.veho.shipment_request as veho
import karrio.schemas.veho.shipment_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if "error" not in response else {}

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response data using typed objects."""
    # Extract shipment data and convert to typed object
    shipment_data = data.get("shipment", {})
    
    if not shipment_data:
        return models.ShipmentDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
        )
    
    # Convert to typed object
    shipment = lib.to_object(shipping.ShipmentData, shipment_data)
    
    tracking_number = shipment.trackingNumber or ""
    shipment_id = shipment.shipmentId or ""
    service_code = shipment.serviceCode or ""
    
    # Extract label data from labelData object
    label_image = None
    label_format = "PDF"
    if shipment.labelData:
        label_data = lib.to_object(shipping.LabelData, shipment.labelData) if isinstance(shipment.labelData, dict) else shipment.labelData
        label_image = label_data.image
        label_format = label_data.format or "PDF"
    
    # Extract invoice image
    invoice_image = shipment.invoiceImage

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type=label_format,
        docs=models.Documents(
            label=label_image,
            invoice=invoice_image,
        ) if label_image or invoice_image else None,
        meta=dict(
            service_code=service_code,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    options = lib.to_shipping_options(payload.options)
    service = provider_units.ShippingService.map(payload.service).value_or_key

    request = {
        "shipper": {
            "addressLine1": shipper.address_line1,
            "city": shipper.city,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "stateCode": shipper.state_code,
            "personName": shipper.person_name,
            "companyName": shipper.company_name,
            "phoneNumber": shipper.phone_number,
            "email": shipper.email,
        },
        "recipient": {
            "addressLine1": recipient.address_line1,
            "city": recipient.city,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "stateCode": recipient.state_code,
            "personName": recipient.person_name,
            "companyName": recipient.company_name,
            "phoneNumber": recipient.phone_number,
            "email": recipient.email,
        },
        "packages": [
            {
                "weight": package.weight.value,
                "weightUnit": package.weight.unit,
                "length": package.length.value if package.length else None,
                "width": package.width.value if package.width else None,
                "height": package.height.value if package.height else None,
                "dimensionUnit": package.dimension_unit if package.dimension_unit else None,
                "packagingType": package.packaging_type or "BOX",
            }
        ],
        "serviceCode": service,
        "labelFormat": payload.label_type or "PDF",
    }

    return lib.Serializable(request, lib.to_dict)
