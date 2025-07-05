"""Karrio ShipEngine rate API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract data from the response to populate the RateDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., RateRequestType),
# while XML schema types don't have this suffix (e.g., RateRequest).

import karrio.schemas.shipengine.rate_request as shipengine_req
import karrio.schemas.shipengine.rate_response as shipengine_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.shipengine.error as provider_error
import karrio.providers.shipengine.units as provider_units
import karrio.providers.shipengine.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    rates = _extract_details(response, settings) if "rates" in response else []

    return rates, errors


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.RateDetails]:
    rates = []
    
    for rate_data in response.get("rates", []):
        rate = lib.to_object(shipengine_res.Rate, rate_data)
        
        if rate:
            rates.append(
                models.RateDetails(
                    carrier_id=settings.carrier_id,
                    carrier_name=rate.carrier_friendly_name or settings.carrier_name,
                    service=rate.service_code,
                    total_charge=rate.shipping_amount.amount,
                    currency=rate.shipping_amount.currency,
                    transit_days=rate.delivery_days,
                    meta=dict(
                        rate_id=rate.rate_id,
                        service_type=rate.service_type,
                        package_type=rate.package_type,
                        zone=rate.zone,
                        guaranteed_service=rate.guaranteed_service,
                        negotiated_rate=rate.negotiated_rate,
                        trackable=rate.trackable,
                        validation_status=rate.validation_status,
                        carrier_code=rate.carrier_code,
                        carrier_nickname=rate.carrier_nickname,
                        service_name=rate.service_code,
                    ),
                )
            )
    
    return rates


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = payload.services
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = shipengine_req.RateRequest(
        ship_from=shipengine_req.Address(
            name=shipper.person_name,
            company_name=shipper.company_name,
            phone=shipper.phone_number,
            address_line1=shipper.address_line1,
            address_line2=shipper.address_line2,
            city_locality=shipper.city,
            state_province=shipper.state_code,
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
        ),
        ship_to=shipengine_req.Address(
            name=recipient.person_name,
            company_name=recipient.company_name,
            phone=recipient.phone_number,
            address_line1=recipient.address_line1,
            address_line2=recipient.address_line2,
            city_locality=recipient.city,
            state_province=recipient.state_code,
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
        ),
        packages=[
            shipengine_req.Package(
                weight=shipengine_req.Weight(
                    value=package.weight.LB,
                    unit="pound",
                ),
                dimensions=shipengine_req.Dimensions(
                    length=package.length.IN,
                    width=package.width.IN,
                    height=package.height.IN,
                    unit="inch",
                ) if package.length and package.width and package.height else None,
                package_code=provider_units.PackagingType.map(package.packaging_type or "package").value,
            )
            for package in packages
        ],
        carrier_ids=options.get("carrier_ids") or settings.config.get("carrier_ids"),
        service_codes=services,
        calculate_tax_amount=options.get("calculate_tax_amount"),
        compare_delivery_dates=options.get("compare_delivery_dates"),
        confirmation=options.get("confirmation"),
        insurance_amount=options.get("insurance_amount"),
        shipment_date=options.get("shipment_date"),
        tags=options.get("tags"),
    )

    return lib.Serializable(request, lib.to_dict)
