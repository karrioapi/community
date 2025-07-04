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
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse ShipEngine rate response and extract rate details.
    
    Args:
        _response: The raw response from ShipEngine API
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
    """Extract rate details from ShipEngine response.
    
    Args:
        response: Parsed response dictionary
        settings: Provider settings
        
    Returns:
        List of rate details
    """
    # For testing purposes, return mock rate details
    # In production, parse actual ShipEngine response structure
    rates = response.get("rate_response", {}).get("rates", [])
    
    return [
        models.RateDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            service=provider_units.get_service_name(
                rate.get("service_code", "standard")
            ),
            currency=rate.get("shipping_amount", {}).get("currency", "USD"),
            total_charge=lib.to_decimal(
                rate.get("shipping_amount", {}).get("amount", "0.00")
            ),
            transit_days=rate.get("estimated_delivery_date"),
            meta=dict(
                service_name=rate.get("service_type"),
                rate_provider="ShipEngine",
                carrier_id=rate.get("carrier_id"),
                rate_id=rate.get("rate_id"),
            ),
        )
        for rate in rates
    ]


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings
) -> lib.Serializable:
    """Create ShipEngine rate request from payload.
    
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

    # Create ShipEngine rate request structure
    request = {
        "rate_options": {
            "carrier_ids": payload.services or [],
            "service_codes": payload.services or [],
            "calculate_tax_amount": True,
            "preferred_currency": "USD",
        },
        "shipment": {
            "ship_from": {
                "name": shipper.person_name,
                "company_name": shipper.company_name,
                "address_line1": shipper.street,
                "address_line2": shipper.address_line2,
                "city_locality": shipper.city,
                "state_province": shipper.state_code,
                "postal_code": shipper.postal_code,
                "country_code": shipper.country_code,
                "phone": shipper.phone_number,
                "address_residential_indicator": "yes" if shipper.residential else "no",
            },
            "ship_to": {
                "name": recipient.person_name,
                "company_name": recipient.company_name,
                "address_line1": recipient.street,
                "address_line2": recipient.address_line2,
                "city_locality": recipient.city,
                "state_province": recipient.state_code,
                "postal_code": recipient.postal_code,
                "country_code": recipient.country_code,
                "phone": recipient.phone_number,
                "address_residential_indicator": "yes" if recipient.residential else "no",
            },
            "packages": [
                {
                    "weight": {
                        "value": package.weight,
                        "unit": "kilogram",
                    },
                    "dimensions": {
                        "length": package.length,
                        "width": package.width,
                        "height": package.height,
                        "unit": "centimeter",
                    },
                    "package_code": provider_units.get_packaging_type(
                        package.packaging_type or "package"
                    ),
                }
            ],
            "advanced_options": {
                option.code: option.state for _, option in options.items()
            },
        },
    }

    return lib.Serializable(request, lib.to_dict)
