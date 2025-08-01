"""Karrio Sendcloud rating API implementation."""

import karrio.schemas.sendcloud.rate_request as sendcloud
import karrio.schemas.sendcloud.rate_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings) 
        for rate in response.get("shipping_methods", [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = lib.to_object(rating.ShippingMethodType, data)
    
    service_name = details.name or "Unknown Service"
    service_code = details.id or "unknown"
    total_charge = details.price.value if details.price else 0.0
    currency = details.price.currency if details.price else "EUR"
    
    charges = []
    
    if details.cost_breakdown:
        for charge_type, amount in details.cost_breakdown.items():
            if amount and amount > 0:
                charges.append(
                    models.ChargeDetails(
                        name=charge_type.replace("_", " ").title(),
                        amount=lib.to_money(amount),
                        currency=currency,
                    )
                )

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_code,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        transit_days=details.transit_time_days,
        extra_charges=charges,
        meta=dict(
            service_name=service_name,
            service_code=service_code,
            carrier_id=details.carrier.id if details.carrier else None,
            carrier_name=details.carrier.name if details.carrier else None,
            min_weight=details.min_weight,
            max_weight=details.max_weight,
            countries=details.countries or [],
            properties=details.properties or {},
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    total_weight = sum(
        package.weight.value * (1000 if package.weight.unit == "KG" else 1)
        for package in packages
    )

    request = sendcloud.RateRequestType(
        to_country=recipient.country_code,
        to_postal_code=recipient.postal_code,
        from_country=shipper.country_code,
        from_postal_code=shipper.postal_code,
        weight=total_weight,
        weight_unit="gram",
        length=max(package.length.CM for package in packages) if packages else 10,
        width=max(package.width.CM for package in packages) if packages else 10,
        height=max(package.height.CM for package in packages) if packages else 10,
        declared_value=lib.to_money(
            sum(
                item.value_amount or 0
                for package in packages
                for item in package.items
            ) or 1.0
        ),
        declared_value_currency=options.currency.state or "EUR",
        service_point_id=options.sendcloud_service_point_id.state,
    )

    return lib.Serializable(request, lib.to_dict)
