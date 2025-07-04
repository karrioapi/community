"""Karrio ShipEngine rate parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.core.units as units
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_rate_response(
    response: lib.Deserializable[typing.Dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = lib.to_dict(response.deserialize())
    messages = error.parse_error_response(response, settings)
    
    rates = [
        _extract_details(rate, settings)
        for rate in responses.get("rate_response", {}).get("rates", [])
    ]
    
    return rates, messages


def _extract_details(
    data: typing.Dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_dict(data)
    service = provider_units.ShippingService.map(rate.get("service_code"))
    
    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        service_type=service.value,
        total_charge=lib.to_decimal(rate.get("shipping_amount", {}).get("amount", 0)),
        currency=rate.get("shipping_amount", {}).get("currency", "USD"),
        estimated_delivery=lib.to_date(rate.get("estimated_delivery_date")),
        meta=dict(
            service_name=service.name_or_key,
            rate_id=rate.get("rate_id"),
            carrier_id=rate.get("carrier_id"),
            carrier_code=rate.get("carrier_code"),
            carrier_friendly_name=rate.get("carrier_friendly_name"),
            zone=rate.get("zone"),
            package_type=rate.get("package_type"),
            delivery_days=rate.get("delivery_days"),
            guaranteed_service=rate.get("guaranteed_service"),
            negotiated_rate=rate.get("negotiated_rate"),
            trackable=rate.get("trackable"),
            validation_status=rate.get("validation_status"),
            **rate,
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
    
    # Get carrier preferences
    carrier_ids = getattr(options, "shipengine_carrier_ids", None)
    service_codes = getattr(options, "shipengine_service_codes", None)
    
    request = dict(
        rate_options=lib.to_dict(
            dict(
                carrier_ids=carrier_ids,
                service_codes=service_codes,
                calculate_tax_amount=True,
                preferred_currency=units.Currency.map(payload.options.get("currency") or "USD").value,
            )
        ),
        shipment=dict(
            ship_to=dict(
                name=recipient.person_name or recipient.company_name,
                company_name=recipient.company_name,
                address_line1=recipient.address_line1,
                address_line2=recipient.address_line2,
                city_locality=recipient.city,
                state_province=recipient.state_code,
                postal_code=recipient.postal_code,
                country_code=recipient.country_code,
                phone=recipient.phone_number,
                email=recipient.email,
            ),
            ship_from=dict(
                name=shipper.person_name or shipper.company_name,
                company_name=shipper.company_name,
                address_line1=shipper.address_line1,
                address_line2=shipper.address_line2,
                city_locality=shipper.city,
                state_province=shipper.state_code,
                postal_code=shipper.postal_code,
                country_code=shipper.country_code,
                phone=shipper.phone_number,
                email=shipper.email,
            ),
            packages=[
                dict(
                    weight=dict(
                        value=float(package.weight.value),
                        unit=package.weight.unit.lower(),
                    ),
                    dimensions=dict(
                        length=float(package.length.value),
                        width=float(package.width.value),
                        height=float(package.height.value),
                        unit=package.dimension_unit.lower(),
                    ),
                    package_code=getattr(package, "packaging_type", None),
                    insured_value=dict(
                        amount=float(package.options.get("insurance", 0) or 0),
                        currency=units.Currency.map(payload.options.get("currency") or "USD").value,
                    ) if package.options.get("insurance") else None,
                )
                for package in packages
            ],
        ),
    )
    
    return lib.Serializable(request) 
