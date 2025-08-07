"""Karrio GLS EU rate API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.gls_eu.error as error
import karrio.providers.gls_eu.utils as provider_utils
import karrio.providers.gls_eu.units as provider_units
import karrio.schemas.gls_eu.rate_request as gls_eu_req
import karrio.schemas.gls_eu.rate_response as gls_eu_res


def parse_rate_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Parse rate response using available schema structure
    rates = [
        _extract_details(rate_data, settings)
        for rate_data in (response.get("rates", []) if isinstance(response, dict) else [])
    ]

    return rates, messages


def _extract_details(
    rate_data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from GLS EU rate response"""
    
    # Convert to typed object for easier access
    rate = lib.to_object(gls_eu_res.RateItem, rate_data)
    
    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=rate.serviceCode or "gls_standard",
        total_charge=lib.to_money(rate.totalCharge or 0),
        currency=rate.currency or "EUR",
        transit_days=rate.transitDays,
        meta=dict(
            service_name=rate.serviceName or "",
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a rate request for GLS EU API"""

    # Convert karrio models to GLS EU format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)

    # Create the GLS EU request object using generated schema
    request = gls_eu_req.SimpleQuoteRequest(
        originationZip=shipper.postal_code,
        deliveryZip=recipient.postal_code,
        packages=[
            gls_eu_req.Package(
                weight=package.weight.value,
                length=package.length.value if package.length else 0,
                width=package.width.value if package.width else 0,
                height=package.height.value if package.height else 0,
            )
            for package in packages
        ],
        serviceClass=services.first.value_or_key if services else "groundPlus",
    )

    return lib.Serializable(request, lib.to_dict)
