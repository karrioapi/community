"""Karrio Veho tracking API implementation."""

import karrio.schemas.veho.tracking_request as veho
import karrio.schemas.veho.tracking_response as tracking

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    # Extract tracking info array and convert each item to typed object
    tracking_info_data = response.get("trackingInfo", []) if isinstance(response, dict) else []
    tracking_details = [
        _extract_details(info_data, settings)
        for info_data in tracking_info_data
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data using typed objects."""
    # Convert to typed object
    tracking_info = lib.to_object(tracking.TrackingInfo, data)
    
    tracking_number = tracking_info.trackingNumber or ""
    status = tracking_info.status or ""
    estimated_delivery = tracking_info.estimatedDelivery
    
    # Extract events from typed objects
    events = []
    if tracking_info.events:
        for event_data in tracking_info.events:
            # Convert event to typed object if it's still a dict
            if isinstance(event_data, dict):
                event = lib.to_object(tracking.TrackingEvent, event_data)
            else:
                event = event_data
                
            events.append({
                "date": event.date or "",
                "time": event.time or "",
                "code": event.code or "",
                "description": event.description or "",
                "location": event.location or ""
            })

    # Map carrier status to karrio standard tracking status
    mapped_status = next(
        (
            status_enum.name
            for status_enum in list(provider_units.TrackingStatus)
            if status in status_enum.value
        ),
        status,
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event["date"]),
                description=event["description"],
                code=event["code"],
                time=event["time"],  # Keep original time format
                location=event["location"],
            )
            for event in events
        ],
        estimated_delivery=lib.fdate(estimated_delivery) if estimated_delivery else None,
        delivered=mapped_status == "delivered" if mapped_status == "delivered" else None,
        status=mapped_status,
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request for the carrier API."""
    tracking_numbers = payload.tracking_numbers
    reference = payload.reference

    request = {
        "trackingNumbers": tracking_numbers,
        "reference": reference,
    }

    return lib.Serializable(request, lib.to_dict)
