"""Karrio SendCloud tracking API implementation."""

import karrio.schemas.sendcloud.tracking_request as sendcloud
import karrio.schemas.sendcloud.tracking_response as tracking

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

    tracking_details = []
    if "parcel" in response and not messages:
        # Extract tracking number from response or context
        tracking_number = response.get("parcel", {}).get("tracking_number")
        tracking_details = [_extract_details(response, settings, tracking_number)]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from SendCloud response."""
    details = lib.to_object(tracking.TrackingResponseType, data)
    parcel = details.parcel

    # Map SendCloud status to Karrio standard tracking status
    status_message = lib.failsafe(lambda: parcel.status.message, "")
    status_id = lib.failsafe(lambda: parcel.status.id, 0)
    
    # SendCloud status mapping
    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if status_message.lower() in [v.lower() for v in status.value]
        ),
        provider_units.TrackingStatus.in_transit.name,
    )

    # Extract tracking events
    events = []
    if parcel.trackingevents:
        for event in parcel.trackingevents:
            events.append(
                models.TrackingEvent(
                    date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%S"),
                    description=event.message,
                    code=event.status,
                    time=lib.ftime(event.timestamp, "%Y-%m-%dT%H:%M:%S"),
                    location=lib.text(
                        event.location.city if event.location else None,
                        event.location.country if event.location else None,
                    ),
                )
            )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number or parcel.trackingnumber,
        events=events,
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=parcel.trackingurl,
            shipment_package_count=1,
            package_weight=lib.failsafe(lambda: float(parcel.weight)),
            package_weight_unit="KG",
        ),
        meta=dict(
            sendcloud_parcel_id=parcel.id,
            sendcloud_status_id=status_id,
            sendcloud_status_message=status_message,
            carrier_code=lib.failsafe(lambda: parcel.carrier.code),
            carrier_name=lib.failsafe(lambda: parcel.carrier.name),
            shipment_id=lib.failsafe(lambda: parcel.shipment.id),
            shipment_name=lib.failsafe(lambda: parcel.shipment.name),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking requests for SendCloud API."""
    # SendCloud tracking is done via GET requests to individual tracking endpoints
    # For now, we'll handle single tracking number at a time
    # The proxy expects tracking_number in context
    
    tracking_number = payload.tracking_numbers[0] if payload.tracking_numbers else None
    carrier = payload.options.get(tracking_number, {}).get("carrier") if tracking_number else None
    
    return lib.Serializable(
        {}, 
        lib.to_dict,
        ctx=dict(
            tracking_number=tracking_number,
            carrier=carrier,
        ),
    )
