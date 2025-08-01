"""Karrio Sendcloud tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    tracking_details = [
        _extract_details(parcel, settings)
        for parcel in response.get("parcels", [])
        if parcel.get("tracking_number")
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking_number = data.get("tracking_number")
    status_code = data.get("status", {}).get("id", 0)
    status_message = data.get("status", {}).get("message", "Unknown")
    
    status = _map_tracking_status(status_code, status_message)
    
    events = []
    for event in data.get("tracking_events", []):
        events.append(
            models.TrackingEvent(
                code=event.get("status_id", ""),
                date=lib.fdate(event.get("timestamp"), "%Y-%m-%dT%H:%M:%S"),
                time=lib.ftime(event.get("timestamp"), "%Y-%m-%dT%H:%M:%S"),
                description=event.get("message", ""),
                location=event.get("location", ""),
            )
        )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        delivered=status == "delivered",
        status=status,
        events=events,
        meta=dict(
            parcel_id=data.get("id"),
            status_code=status_code,
            status_message=status_message,
            carrier=data.get("carrier", {}),
            service_point=data.get("service_point"),
        ),
    )


def _map_tracking_status(status_code: int, status_message: str) -> str:
    """Map Sendcloud status codes to Karrio tracking status."""
    status_mapping = {
        1: "announced",
        2: "announced",
        3: "announced",
        4: "announced",
        5: "announced",
        6: "announced",
        7: "ready_to_be_shipped",
        8: "ready_to_be_shipped",
        11: "in_transit",
        12: "in_transit",
        13: "out_for_delivery",
        14: "out_for_delivery",
        15: "delivered",
        16: "delivered",
        17: "delivery_failed",
        18: "delivery_failed",
        19: "delivery_failed",
        20: "ready_to_be_collected",
        21: "delivered",
        22: "no_show",
        23: "unable_to_deliver",
        24: "unable_to_deliver",
        999: "delivery_failed",
    }
    
    sendcloud_status = status_mapping.get(status_code, "in_transit")
    
    for karrio_status in provider_units.TrackingStatus:
        if sendcloud_status in karrio_status.value:
            return karrio_status.name
    
    return provider_units.TrackingStatus.in_transit.name


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking request for Sendcloud."""
    
    tracking_numbers = payload.tracking_numbers
    
    request = {
        "tracking_numbers": tracking_numbers,
    }

    return lib.Serializable(request, lib.to_dict)
