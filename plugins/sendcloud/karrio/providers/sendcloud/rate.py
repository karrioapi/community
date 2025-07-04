"""Karrio SendCloud rating API implementation."""

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
    rates = [_extract_details(rate, settings) for rate in response.get("shipping_products", [])]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = lib.to_object(rating.ShippingProductType, data)
    service_code = details.code or "sendcloud_standard"
    service = provider_units.ShippingServiceID.map(service_code)
    
    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.value_or_key,
        total_charge=lib.to_money(details.price),
        currency="EUR",  # SendCloud typically uses EUR
        transit_days=None,  # SendCloud doesn't provide transit days in rates
        extra_charges=[],
        meta=dict(
            rate_provider=details.carrier,
            sendcloud_code=details.code,
            service_name=details.name,
            sendcloud_service_point_input=details.service_point_input,
            min_weight=details.min_weight,
            max_weight=details.max_weight,
            countries=details.countries,
            methods=details.methods,
            status=details.status,
            functionalities=details.functionalities,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    weight_unit, dimension_unit = packages.compatible_units
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to sendcloud specific type
    request = sendcloud.RateRequestType(
        from_address=sendcloud.AddressType(
            name=shipper.person_name or "N/A",
            company=shipper.company_name,
            address_line_1=shipper.address_line1,
            address_line_2=shipper.address_line2,
            city=shipper.city,
            state=shipper.state_code,
            postal_code=shipper.postal_code,
            country=shipper.country_code,
        ),
        to_address=sendcloud.AddressType(
            name=recipient.person_name or "N/A",
            company=recipient.company_name,
            address_line_1=recipient.address_line1,
            address_line_2=recipient.address_line2,
            city=recipient.city,
            state=recipient.state_code,
            postal_code=recipient.postal_code,
            country=recipient.country_code,
        ),
        parcels=[
            sendcloud.ParcelType(
                height=package.height.value,
                length=package.length.value,
                width=package.width.value,
                weight=package.weight.value,
            )
            for package in packages
        ],
        service_points=lib.identity(
            [
                sendcloud.ServicePointType(
                    code=options.sendcloud_service_point_id.state,
                    carrier="sendcloud",
                )
            ]
            if options.sendcloud_service_point_id.state
            else []
        ),
        to_service_point=lib.identity(
            options.sendcloud_service_point_id.state
            if options.sendcloud_service_point_id.state
            else None
        ),
        from_service_point=None,
    )

    return lib.Serializable(request, lib.to_dict) 
