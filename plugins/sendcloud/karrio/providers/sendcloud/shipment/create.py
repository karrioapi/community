"""Karrio Sendcloud shipment API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units
# CRITICAL: Always import and use the generated schema types
import karrio.schemas.sendcloud.shipment_request as sendcloud_req
import karrio.schemas.sendcloud.shipment_response as sendcloud_res


def parse_shipment_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Convert to typed object using generated schema
    shipment_response = lib.to_object(sendcloud_res.ShipmentResponseType, response)
    
    shipment = None
    if shipment_response.parcel:
        shipment = _extract_details(lib.to_dict(shipment_response.parcel), settings, _response.ctx)

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    """Extract shipment details from Sendcloud response data"""

    # Convert the Sendcloud data to a proper object for easy attribute access
    parcel = lib.to_object(sendcloud_res.ParcelType, data)
    
    tracking_number = parcel.tracking_number if hasattr(parcel, 'tracking_number') else None
    parcel_id = str(parcel.id) if hasattr(parcel, 'id') and parcel.id else None
    
    # Extract label information
    label_url = None
    label_content = None
    label_type = "PDF"
    
    if hasattr(parcel, 'label') and parcel.label:
        if hasattr(parcel.label, 'label_printer'):
            label_url = parcel.label.label_printer
        
        # Download label content if URL is available
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
        shipment_identifier=parcel_id,
        docs=models.Documents(
            label=label_content,
        ),
        meta=dict(
            parcel_id=parcel_id,
            label_url=label_url,
            label_type=label_type,
            service_name="Sendcloud",
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the Sendcloud API"""

    # Convert karrio models to Sendcloud-specific format
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

    total_weight = sum(
        package.weight.value * (1000 if package.weight.unit == "KG" else 1)
        for package in packages
    )

    # Create parcel items using generated schema types
    parcel_items = [
        sendcloud_req.ParcelItemType(
            description=item.description or item.title or "Item",
            quantity=item.quantity or 1,
            weight=str(int(item.weight.value * (1000 if item.weight.unit == "KG" else 1))) if item.weight else "100",
            value=str(item.value_amount or 1.0),
            hs_code=item.hs_code or "",
            origin_country=item.origin_country or shipper.country_code,
        )
        for package in packages
        for item in (package.items or [models.Commodity(
            title="Package",
            description=package.description or "Package",
            quantity=1,
            weight=package.weight.value,
            value_amount=1.0,
        )])
    ]

    # Create the Sendcloud-specific request object using generated types
    parcel = sendcloud_req.ParcelType(
        name=recipient.person_name or recipient.company_name or "Customer",
        company_name=recipient.company_name or "",
        address=recipient.address_line1,
        address_2=recipient.address_line2 or "",
        city=recipient.city,
        postal_code=recipient.postal_code,
        country=recipient.country_code,
        telephone=recipient.phone_number or "",
        email=recipient.email or "",
        weight=str(int(total_weight)),
        order_number=options.sendcloud_order_number.state or payload.reference or "",
        parcel_items=parcel_items,
        service_point_id=options.sendcloud_service_point_id.state,
        require_signature=options.sendcloud_require_signature.state,
        insured_value=options.sendcloud_insured_value.state,
        reference=options.sendcloud_reference.state,
        shipping_method=payload.service,
    )

    # Add customs declaration if needed
    if customs and customs.duty:
        parcel.customs_declaration = sendcloud_req.CustomsDeclarationType(
            contents=options.sendcloud_contents.state or customs.content_type or "goods",
            invoice_nr=options.sendcloud_customs_invoice_nr.state or "",
            non_delivery="return",
            shipment_type=options.sendcloud_customs_shipment_type.state or "commercial_goods",
        )

    request = sendcloud_req.ShipmentRequestType(parcel=parcel)

    return lib.Serializable(request, lib.to_dict)
