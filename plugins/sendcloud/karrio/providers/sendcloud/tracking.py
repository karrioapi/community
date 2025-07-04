"""Karrio SendCloud tracking API implementation."""

import karrio.schemas.sendcloud.tracking_request as sendcloud
import karrio.schemas.sendcloud.tracking_response as tracking

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()
    messages: typing.List[models.Message] = []
    tracking_details: typing.List[models.TrackingDetails] = []
    
    for tracking_number, response in responses:
        errors = error.parse_error_response(response, settings)
        messages.extend(errors)
        
        if not errors:
            tracking_info = response.get("tracking", {})
            
            details = models.TrackingDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                tracking_number=tracking_number,
                events=[
                    models.TrackingEvent(
                        date=lib.fdate(event.get("timestamp"), "%Y-%m-%d %H:%M:%S"),
                        description=event.get("message", ""),
                        location=event.get("location", ""),
                        code=event.get("status", ""),
                        time=lib.ftime(event.get("timestamp"), "%Y-%m-%d %H:%M:%S"),
                    )
                    for event in tracking_info.get("tracking_events", [])
                ],
                status=lib.identity(
                    provider_units.TrackingStatus.map(
                        tracking_info.get("status", "")
                    ).value
                ),
                estimated_delivery=None,
                meta=dict(
                    carrier=tracking_info.get("carrier", ""),
                    code=tracking_info.get("code", ""),
                    message=tracking_info.get("message", ""),
                    updated=tracking_info.get("updated", ""),
                ),
            )
            tracking_details.append(details)
    
    return tracking_details, messages


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    
    request = [
        sendcloud.TrackingRequestType(
            tracking_number=tracking_number,
            carrier=None,
            postal_code=None,
        )
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict) 
