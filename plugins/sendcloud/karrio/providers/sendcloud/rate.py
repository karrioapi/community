"""Karrio SendCloud rate API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract data from the response to populate the RateDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., RateRequestType),
# while XML schema types don't have this suffix (e.g., RateRequest).

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as provider_error
import karrio.providers.sendcloud.units as provider_units
import karrio.providers.sendcloud.utils as provider_utils


def parse_rate_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse SendCloud rate response and extract rate details.
    
    Args:
        _response: The raw response from SendCloud API
        settings: Provider settings
        
    Returns:
        Tuple of rate details list and error messages
    """
    response = _response.deserialize()
    errors = provider_error.parse_error_response(response, settings)
    rates = _extract_details(response, settings) if "error" not in response else []

    return rates, errors


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.RateDetails]:
    """Extract rate details from SendCloud response.
    
    Args:
        response: Parsed response dictionary
        settings: Provider settings
        
    Returns:
        List of rate details
    """
    # For testing purposes, return mock rate details
    # In production, parse actual SendCloud response structure
    rates = response.get("rates", [])
    
    return [
        models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=provider_units.get_service_name(
                rate.get("service", "standard")
            ),
            currency=rate.get("currency", "USD"),
            total_charge=lib.to_decimal(rate.get("total_charge", "0.00")),
            transit_days=rate.get("transit_days"),
            meta=dict(
                service_name=rate.get("service_name"),
                rate_provider="SendCloud",
            ),
        )
        for rate in rates
    ]


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings
) -> lib.Serializable:
    """Create SendCloud rate request from payload.
    
    Args:
        payload: Rate request payload
        settings: Provider settings
        
    Returns:
        Serializable request object
    """
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

    # Create simplified request structure for SendCloud
    request = {
        "from_address": {
            "name": shipper.person_name,
            "company": shipper.company_name,
            "street1": shipper.street,
            "street2": shipper.address_line2,
            "city": shipper.city,
            "state": shipper.state_code,
            "postal_code": shipper.postal_code,
            "country": shipper.country_code,
            "phone": shipper.phone_number,
            "email": shipper.email,
        },
        "to_address": {
            "name": recipient.person_name,
            "company": recipient.company_name,
            "street1": recipient.street,
            "street2": recipient.address_line2,
            "city": recipient.city,
            "state": recipient.state_code,
            "postal_code": recipient.postal_code,
            "country": recipient.country_code,
            "phone": recipient.phone_number,
            "email": recipient.email,
        },
        "parcel": {
            "weight": package.weight,
            "weight_unit": "kg",
            "length": package.length,
            "width": package.width,
            "height": package.height,
            "packaging_type": provider_units.get_packaging_type(
                package.packaging_type or "package"
            ),
        },
        "options": {option.code: option.state for _, option in options.items()},
        "reference": payload.reference,
    }

    return lib.Serializable(request, lib.to_dict)
