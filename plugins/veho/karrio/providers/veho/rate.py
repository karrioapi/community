"""Karrio Veho rate API implementation."""

import karrio.schemas.veho.rate_request as veho_req
import karrio.schemas.veho.rate_response as veho_res

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
    
    # Veho API returns an array of SimpleQuoteItem objects directly
    rate_objects = response if isinstance(response, list) else []
    rates = [_extract_details(rate, settings) for rate in rate_objects]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from Veho SimpleQuoteItem response data."""
    quote = lib.to_object(veho_res.SimpleQuoteItem, data)

    # Map Veho service class to our internal service name
    service = quote.serviceClass or "groundPlus"
    service_name = provider_units.get_service_name(service)
    total = float(quote.rate) if quote.rate else 0.0
    currency = quote.currency or "USD"
    transit_days = int(quote.transitTime) if quote.transitTime else None

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service,
        total_charge=lib.to_money(total),
        currency=currency,
        transit_days=transit_days,
        meta=dict(
            service_name=service_name,
            quote_id=quote.quoteId,
            assumed_injection_zip=quote.assumedInjectionZip,
            billable_weight=quote.billableWeight,
            zone=quote.zone,
            ship_date=quote.shipDate,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a SimpleQuoteRequest for the Veho API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    # Use the requested service or default to groundPlus
    service = services.first or provider_units.ShippingService.veho_ground_plus

    request = veho_req.SimpleQuoteRequest(
        originationZip=shipper.postal_code,
        deliveryZip=recipient.postal_code,
        packages=[
            veho_req.Package(
                length=package.length.CM,
                width=package.width.CM,
                height=package.height.CM,
                weight=package.weight.LB,  # Veho uses pounds
            )
            for package in packages
        ],
        shipDate=lib.fdatetime(options.shipment_date.state, "%Y-%m-%d") if options.shipment_date.state else None,
        serviceClass=service.value,
    )

    return lib.Serializable(request, lib.to_dict)
