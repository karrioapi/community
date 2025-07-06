"""Karrio ShipEngine rate API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units
import karrio.schemas.shipengine.rate_request as shipengine_req
import karrio.schemas.shipengine.rate_response as shipengine_res


def parse_rate_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rate_response_obj = lib.to_object(shipengine_res.RateResponseType, response)

    # Update dynamic services
    lib.identity(
        provider_units.ShippingService.update_from_response(response.get("rate_response", {}))
        if rate_response_obj.rate_response else None
    )

    rates = []
    if rate_response_obj.rate_response and rate_response_obj.rate_response.rates:
        rates = [
            _extract_rate_details(lib.to_dict(rate), settings)
            for rate in rate_response_obj.rate_response.rates
        ]

    return rates, messages


def _extract_rate_details(
    rate_data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(shipengine_res.RateType, rate_data)
    
    amounts = [
        rate.shipping_amount,
        rate.insurance_amount, 
        rate.confirmation_amount,
        rate.other_amount,
    ]
    
    total_amount = sum(
        lib.to_money(amount.amount)
        for amount in amounts if amount and amount.amount
    )
    
    currency = next(
        (amount.currency for amount in amounts if amount and amount.currency), 
        "USD"
    )
    
    service_key = lib.identity(
        f"shipengine_{rate.carrier_code}_{rate.service_code}"
        if all([rate.carrier_code, rate.service_code])
        else rate.service_code or ""
    )

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service_key,
        total_charge=lib.to_money(total_amount),
        currency=currency,
        transit_days=rate.delivery_days,
        meta=dict(
            service_name=rate.service_type,
            carrier_code=rate.carrier_code,
            carrier_name=rate.carrier_friendly_name,
            rate_id=rate.rate_id,
            carrier_id=rate.carrier_id,
            estimated_delivery_date=rate.estimated_delivery_date,
            guaranteed_service=rate.guaranteed_service or False,
            trackable=rate.trackable or True,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = shipengine_req.RateRequestType(
        rate_options=shipengine_req.RateOptionsType(
            calculate_tax_amount=True,
            preferred_currency="USD",
        ),
        shipment=shipengine_req.ShipmentType(
            validate_address="validate_and_clean",
            ship_to=shipengine_req.ShipType(
                name=recipient.person_name,
                phone=recipient.phone_number,
                company_name=recipient.company_name,
                address_line1=recipient.address_line1,
                address_line2=recipient.address_line2,
                address_line3=recipient.address_line3,
                city_locality=recipient.city,
                state_province=recipient.state_code,
                postal_code=lib.failsafe(lambda: int(recipient.postal_code)) if recipient.postal_code and recipient.postal_code.isdigit() else None,
                country_code=recipient.country_code,
                address_residential_indicator="yes" if recipient.residential else "no",
            ),
            ship_from=shipengine_req.ShipType(
                name=shipper.person_name,
                phone=shipper.phone_number,
                company_name=shipper.company_name,
                address_line1=shipper.address_line1,
                address_line2=shipper.address_line2,
                address_line3=shipper.address_line3,
                city_locality=shipper.city,
                state_province=shipper.state_code,
                postal_code=lib.failsafe(lambda: int(shipper.postal_code)) if shipper.postal_code and shipper.postal_code.isdigit() else None,
                country_code=shipper.country_code,
                address_residential_indicator="yes" if shipper.residential else "no",
            ),
            packages=[
                shipengine_req.PackageType(
                    weight=shipengine_req.WeightType(
                        value=package.weight.value,
                        unit=lib.failsafe(lambda: provider_units.WeightUnit[package.weight.unit].value, "pound"),
                    ),
                    dimensions=lib.identity(
                        shipengine_req.DimensionsType(
                            unit=lib.failsafe(lambda: provider_units.DimensionUnit[package.dimension_unit or "IN"].value, "inch"),
                            length=package.length.value,
                            width=package.width.value,
                            height=package.height.value,
                        ) if all([package.length, package.width, package.height]) else None
                    ),
                    package_code=lib.failsafe(
                        lambda: provider_units.PackagingType[package.packaging_type or "package"].value, "package"
                    ),
                )
                for package in packages
            ],
        ),
    )

    return lib.Serializable(request, lib.to_dict)

