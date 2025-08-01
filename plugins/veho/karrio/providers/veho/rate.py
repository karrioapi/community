"""Karrio Veho rate API implementation."""

import karrio.schemas.veho.rate_request as veho
import karrio.schemas.veho.rate_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings)
        for rate in response
        if isinstance(response, list)
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.SimpleQuoteItem, data)
    service = provider_units.ShippingService.map(rate.serviceClass)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.rate),
        currency=rate.currency or "USD",
        transit_days=lib.to_int(rate.transitTime),
        meta=dict(quote_id=rate.quoteId),
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

    service = (
        lib.to_services(payload.services, provider_units.ShippingService).first
        or provider_units.ShippingService.ground_plus
    )

    request = veho.SimpleQuoteRequest(
        originationZip=shipper.postal_code,
        deliveryZip=recipient.postal_code,
        packages=[
            veho.Package(
                length=package.length.CM,
                width=package.width.CM,
                height=package.height.CM,
                weight=package.weight.LB,
            )
            for package in packages
        ],
        shipDate=options.shipment_date.state or lib.fdatetime(
            options.shipment_date.default
        ).strftime("%Y-%m-%d"),
        serviceClass=service.value,
    )

    return lib.Serializable(request, lib.to_dict)
