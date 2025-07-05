"""
SendCloud Rate Provider - API v2/v3 JSON Implementation
"""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units
import karrio.schemas.sendcloud.parcel_request as sendcloud
import karrio.schemas.sendcloud.parcel_response as shipping


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    rates = _extract_details(response, settings) if "parcel" in response else []

    return rates, errors


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.RateDetails]:
    parcel = lib.to_object(shipping.Parcel, response.get("parcel"))
    
    if not parcel.shipment:
        return []
    
    service_info = provider_units.Service.info(parcel.shipment.id, parcel.shipment.name)
    
    return [
        models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=service_info[0],
            currency="EUR",
            total_charge=lib.to_decimal(parcel.total_order_value or "0"),
            meta=dict(
                service_name=service_info[1],
                shipment_id=parcel.shipment.id,
                shipment_name=parcel.shipment.name,
            ),
        )
    ]


def rate_request(payload: models.RateRequest, settings: provider_utils.Settings) -> lib.Serializable:
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
    
    service = provider_units.ShippingService.map(payload.services[0] if payload.services else "standard")
    
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
            request_label=False,
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
