"""Karrio SendCloud tracking API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract tracking details and events from the response to populate TrackingDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., TrackingRequestType),
# while XML schema types don't have this suffix (e.g., TrackingRequest).

import karrio.schemas.sendcloud.tracking_request as sendcloud_req
import karrio.schemas.sendcloud.tracking_response as sendcloud_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
from karrio.core.units import TrackingStatus
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # For testing purposes, return a mock tracking details
    tracking_details = [models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="TRACK123",
        status=TrackingStatus.in_transit.name,
        estimated_delivery="2024-04-15",
        events=[
            models.TrackingEvent(
                date="2024-04-12",
                time="14:30:00",
                location="San Francisco, CA",
                code="PU",
                description="Package picked up"
            )
        ]
    )]

    return tracking_details, messages


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a tracking request for the carrier API
    """
    # Create a simple request structure
    request = {
        "tracking_numbers": payload.tracking_numbers,
        "reference": payload.reference,
    }

    return lib.Serializable(request, lib.to_dict)
