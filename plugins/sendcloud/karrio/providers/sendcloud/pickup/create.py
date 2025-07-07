"""Karrio SendCloud pickup API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """Parse pickup response from SendCloud API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Extract pickup details if successful
    pickup = _extract_details(response, settings) if not messages else None

    return pickup, messages


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from SendCloud response."""
    pickup_id = response.get("id")
    pickup_date = response.get("pickup_date")
    
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=str(pickup_id),
        pickup_date=lib.fdate(pickup_date),
        pickup_charge=lib.to_money(0),
        ready_time=lib.ftime(response.get("ready_time")),
        closing_time=lib.ftime(response.get("closing_time")),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a pickup request for SendCloud API."""
    return lib.Serializable(
        dict(
            pickup_date=lib.fdate(payload.pickup_date),
            ready_time=lib.ftime(payload.ready_time),
            closing_time=lib.ftime(payload.closing_time),
            address=dict(
                company_name=payload.address.company_name,
                contact_name=payload.address.person_name,
                address_line1=payload.address.address_line1,
                city=payload.address.city,
                postal_code=payload.address.postal_code,
                country_code=payload.address.country_code,
                phone_number=payload.address.phone_number,
                email=payload.address.email,
            ),
            parcels=payload.parcels,
        ),
        lib.to_dict,
    )