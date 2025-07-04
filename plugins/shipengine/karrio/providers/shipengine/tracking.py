"""Karrio ShipEngine tracking parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_tracking_response(
    response: lib.Deserializable[typing.Dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = lib.to_dict(response.deserialize())
    messages = error.parse_error_response(response, settings)
    
    tracking_details = [
        _extract_details(tracking, settings)
        for tracking in responses
        if isinstance(tracking, tuple) and len(tracking) == 2
    ]
    
    return tracking_details, messages


def _extract_details(
    data: typing.Tuple[str, typing.Dict],
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking_number, tracking_info = data
    tracking = lib.to_dict(tracking_info)
    
    status = provider_units.TrackingStatus.map(tracking.get("status_code", "UNKNOWN"))
    
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        status=status.name,
        estimated_delivery=lib.to_date(tracking.get("estimated_delivery_date")),
        delivered=tracking.get("actual_delivery_date") is not None,
        events=[
            models.TrackingEvent(
                code=event.get("event_code"),
                description=event.get("description"),
                date=lib.to_date(event.get("occurred_at")),
                time=lib.to_time(event.get("occurred_at")),
                location=lib.to_location(
                    dict(
                        city=event.get("city_locality"),
                        state_code=event.get("state_province"),
                        postal_code=event.get("postal_code"),
                        country_code=event.get("country_code"),
                    )
                ),
            )
            for event in tracking.get("events", [])
        ],
        meta=dict(
            carrier_status_code=tracking.get("carrier_status_code"),
            carrier_status_description=tracking.get("carrier_status_description"),
            ship_date=tracking.get("ship_date"),
            actual_delivery_date=tracking.get("actual_delivery_date"),
            exception_description=tracking.get("exception_description"),
            tracking_url=tracking.get("tracking_url"),
            **tracking,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        dict(
            tracking_number=tracking_number,
            carrier_code=None,  # ShipEngine can auto-detect carrier
        )
        for tracking_number in payload.tracking_numbers
    ]
    
    return lib.Serializable(request) 
