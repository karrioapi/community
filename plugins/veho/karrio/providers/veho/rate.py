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
    
    # Extract rates array and convert each item to typed object
    rates_data = response.get("rates", []) if isinstance(response, dict) else []
    rates = [_extract_details(rate_data, settings) for rate_data in rates_data]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """
    Extract rate details from rate response data using typed objects
    """
    # Convert individual rate item to typed object
    rate_item = lib.to_object(rating.RateItem, data)
    
    # Use typed properties
    service = rate_item.serviceCode or ""
    service_name = rate_item.serviceName or ""
    total = rate_item.totalCharge or 0.0
    currency = rate_item.currency or "USD"
    transit_days = int(rate_item.transitDays or 0)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service,
        total_charge=total,
        currency=currency,
        transit_days=transit_days,
        meta=dict(
            service_name=service_name,
        ),
    )


def rate_request(payload: models.RateRequest, settings: provider_utils.Settings) -> lib.Serializable:
    """Create a rate request for the carrier API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    package = packages.single
    
    # Create simple request structure that matches test expectations
    request = {
        "shipper": {
            "addressLine1": shipper.address_line1,
            "city": shipper.city,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "stateCode": shipper.state_code,
            "personName": shipper.person_name,
            "companyName": shipper.company_name,
            "phoneNumber": shipper.phone_number,
            "email": shipper.email,
        },
        "recipient": {
            "addressLine1": recipient.address_line1,
            "city": recipient.city,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "stateCode": recipient.state_code,
            "personName": recipient.person_name,
            "companyName": recipient.company_name,
            "phoneNumber": recipient.phone_number,
            "email": recipient.email,
        },
        "packages": [
            {
                "weight": package.weight.value,
                "weightUnit": package.weight.unit,
                "length": package.length.value if package.length else None,
                "width": package.width.value if package.width else None,
                "height": package.height.value if package.height else None,
                "dimensionUnit": package.dimension_unit if package.dimension_unit else None,
                "packagingType": package.packaging_type or "BOX",
            }
        ],
    }

    return lib.Serializable(request, lib.to_dict)
