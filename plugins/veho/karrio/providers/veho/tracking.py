"""Karrio Veho tracking API implementation."""

import karrio.schemas.veho.tracking_request as veho_req
import karrio.schemas.veho.tracking_response as veho_res

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
    
    # Handle the trackingInfo array structure
    tracking_info = response.get("trackingInfo", [])
    tracking_details = [
        _extract_details(details, settings)
        for details in tracking_info
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    """Extract tracking details from carrier response data."""
    tracking_number = data.get("trackingNumber", "")
    status = data.get("status", "")
    status_details = data.get("statusDetails", "")
    estimated_delivery = data.get("estimatedDelivery")
    
    # Extract events
    events = []
    if "events" in data and data["events"]:
        for event in data["events"]:
            events.append({
                "date": event.get("date", ""),
                "time": event.get("time", ""),
                "code": event.get("code", ""),
                "description": event.get("description", ""),
                "location": event.get("location", "")
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
