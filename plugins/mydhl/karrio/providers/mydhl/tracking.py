"""Karrio MyDHL tracking API implementation."""

import karrio.schemas.mydhl.tracking_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.units as provider_units
import karrio.providers.mydhl.utils as provider_utils


def parse_tracking_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    # Response is a list of (tracking_number, tracking_data) tuples
    messages = []
    tracking_details = []
    
    for tracking_number, tracking_data in response:
        if tracking_data:
            # Check for errors in individual tracking responses
            response_messages = error.parse_error_response(tracking_data, settings)
            messages.extend(response_messages)
            
            # Only process if no errors
            if not response_messages:
                details = _extract_details(tracking_data, settings, tracking_number)
                tracking_details.append(details)

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str,
) -> models.TrackingDetails:
    # Extract tracking info from simple JSON response
    tracking_info = data.get("trackingInfo", [])
    
    if not tracking_info:
        return models.TrackingDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking_number=tracking_number,
            events=[],
            status="in_transit",
        )
    
    track_info = tracking_info[0]
    events = track_info.get("events", [])
    
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=track_info.get("trackingNumber", tracking_number),
        events=[
            models.TrackingEvent(
                date=event.get("date"),
                time=event.get("time"),
                description=event.get("description"),
                location=event.get("location"),
                code=event.get("code"),
            )
            for event in events
        ],
        status=track_info.get("status", "in_transit"),
        estimated_delivery=track_info.get("estimatedDelivery"),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking request with tracking numbers."""
    request = {
        "trackingNumbers": payload.tracking_numbers,
        "reference": payload.reference,
    }

    return lib.Serializable(request, lib.to_dict)