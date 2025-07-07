"""Karrio SendCloud shipment API implementation."""

import karrio.schemas.sendcloud.shipment_request as sendcloud
import karrio.schemas.sendcloud.shipment_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data (either parcel object or flat response)
    has_shipment = (
        ("parcel" in response and response["parcel"] is not None) or
        ("tracking_number" in response or "shipment_id" in response)
    )

    shipment = _extract_details(response, settings) if has_shipment else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from SendCloud response."""
    
    # Extract basic shipment information
    tracking_number = data.get("tracking_number")
    shipment_id = data.get("shipment_id")
    label_format = data.get("label_format", "PDF")
    service_code = data.get("service_code")
    
    # Extract label and invoice data
    label_data = data.get("label_image")
    invoice_data = data.get("invoice_image")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type=label_format,
        docs=models.Documents(
            label=label_data,
            invoice=invoice_data,
        ),
        meta=dict(
            service_code=service_code,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for SendCloud's parcel API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    
    # Parse service to extract carrier and method
    service_parts = (payload.service or "").split("_", 2)
    shipping_method_id = None
    if len(service_parts) >= 3 and service_parts[0] == "sendcloud":
        # Extract shipping method ID from composite service
        # e.g., sendcloud_postnl_standard -> need to find method ID
        carrier_code = service_parts[1]
        product_code = service_parts[2]
        # In production, this would be mapped from rate response metadata
        
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # SendCloud expects total weight
    total_weight = sum(pkg.weight.KG for pkg in packages)
    
    # Get max dimensions
    max_length = max((pkg.length.CM for pkg in packages if pkg.length), default=0)
    max_width = max((pkg.width.CM for pkg in packages if pkg.width), default=0)
    max_height = max((pkg.height.CM for pkg in packages if pkg.height), default=0)

    # Handle customs for international shipments using proper schema types
    customs_items = []
    if payload.customs:
        customs_items = [
            sendcloud.ParcelItemType(
                description=item.description or item.title,
                quantity=item.quantity,
                weight=str(item.weight),
                value=str(item.value_amount),
                hscode=item.hs_code,
                origincountry=item.origin_country or shipper.country_code,
                sku=item.sku,
                productid=item.metadata.get("product_id"),
            )
            for item in payload.customs.commodities
        ]

    # Map data to SendCloud shipment request format
    request = sendcloud.ShipmentRequestType(
        name=recipient.person_name or recipient.company_name,
        address=recipient.address_line1,
        address2=recipient.address_line2,
        housenumber=lib.failsafe(lambda: int(recipient.street_number)),
        city=recipient.city,
        postalcode=recipient.postal_code,
        country=recipient.country_code,
        companyname=recipient.company_name,
        email=recipient.email,
        telephone=recipient.phone_number,
        weight=str(total_weight),
        length=int(max_length) if max_length > 0 else None,
        width=int(max_width) if max_width > 0 else None,
        height=int(max_height) if max_height > 0 else None,
        requestlabel=lib.identity(
            options.sendcloud_request_label.state
            if options.sendcloud_request_label.state is not None
            else True
        ),
        applyshippingrules=lib.identity(
            settings.connection_config.apply_shipping_rules.state
            if settings.connection_config.apply_shipping_rules.state is not None
            else True
        ),
        shippingmethod=shipping_method_id,
        externalreference=payload.reference,
        ordernumber=lib.failsafe(lambda: payload.metadata.get("order_number")),
        insuredvalue=options.insurance.state,
        totalinsuredvalue=options.insurance.state,
        senderaddress=lib.identity(
            # In production, sender addresses would be pre-configured in SendCloud
            int(payload.metadata.get("sender_address_id"))
            if "sender_address_id" in (payload.metadata or {})
            else None
        ),
        shipmentuuid=lib.failsafe(lambda: payload.metadata.get("shipment_uuid")),
        customsinvoicenr=lib.identity(
            payload.customs.invoice
            if payload.customs and payload.customs.invoice
            else None
        ),
        customsshipmenttype=lib.identity(
            # Map Karrio customs content type to SendCloud type ID
            # 1: Gift, 2: Documents, 3: Commercial Goods, 4: Commercial Sample, 5: Return
            {
                "gift": 1,
                "documents": 2,
                "merchandise": 3,
                "sample": 4,
                "return_merchandise": 5,
            }.get(payload.customs.content_type, 3)
            if payload.customs
            else None
        ),
        parcelitems=customs_items if customs_items else None,
    )

    return lib.Serializable(request, lib.to_dict)
