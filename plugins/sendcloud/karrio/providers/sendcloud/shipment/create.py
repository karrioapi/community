"""
SendCloud Shipment Create Provider - API v2/v3 JSON Implementation
"""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units
import karrio.schemas.sendcloud.parcel_request as sendcloud
import karrio.schemas.sendcloud.parcel_response as shipping


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if "parcel" in response else None

    return shipment, errors


def _extract_details(
    response: dict, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    parcel = lib.to_object(shipping.Parcel, response.get("parcel"))

    label_url = None
    if parcel.label and parcel.label.normal_printer:
        label_url = parcel.label.normal_printer[0]

    tracking_url = getattr(parcel, "tracking_url", None)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        shipment_identifier=str(parcel.id),
        tracking_number=parcel.tracking_number,
        label_type="PDF",
        docs=models.Documents(
            label=provider_utils.download_label(label_url) if label_url else None
        ),
        meta=dict(
            tracking_url=tracking_url,
            carrier_tracking_link=tracking_url,
            service_name=parcel.shipment.name if parcel.shipment else None,
            label_url=label_url,
            parcel_id=parcel.id,
            reference=parcel.reference,
        ),
    )


def shipment_request(payload: models.ShipmentRequest, settings: provider_utils.Settings) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
    ).single

    options = lib.to_shipping_options(
        payload,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    service = provider_units.ShippingService.map(payload.service or "standard")

    parcel_items = []
    if package.parcel.items:
        for item in package.parcel.items:
            parcel_items.append(
                sendcloud.ParcelItem(
                    description=item.description or item.title or "Item",
                    quantity=item.quantity,
                                         weight=str(units.Weight(item.weight, item.weight_unit).KG),
                    value=str(item.value_amount or 0),
                    hs_code=item.hs_code,
                    origin_country=item.origin_country,
                    product_id=item.id,
                    sku=item.sku,
                    properties=item.metadata,
                )
            )

    if not parcel_items:
        parcel_items = [
            sendcloud.ParcelItem(
                description=package.parcel.content or "Package",
                quantity=1,
                weight=str(package.weight.KG),
                value="0",
            )
        ]

    request = sendcloud.ParcelRequest(
        parcel=sendcloud.ParcelData(
            name=recipient.person_name,
            company_name=recipient.company_name,
            email=recipient.email,
            telephone=recipient.phone_number,
            address=recipient.street,
            house_number=recipient.address_line2 or "1",
            address_2=recipient.address_line2,
            city=recipient.city,
            country=recipient.country_code,
            postal_code=recipient.postal_code,
            weight=str(package.weight.KG),
            length=str(package.length.CM) if package.length else None,
            width=str(package.width.CM) if package.width else None,
            height=str(package.height.CM) if package.height else None,
            parcel_items=parcel_items,
            request_label=payload.label_type is not None,
            apply_shipping_rules=False,
            shipment=sendcloud.Shipment(
                id=service.value,
                name=service.name,
            ) if service else None,
            sender_address=getattr(settings, "sender_address", None),
            total_order_value="0",
            total_order_value_currency="EUR",
        )
    )

    return lib.Serializable(request, lib.to_dict)
