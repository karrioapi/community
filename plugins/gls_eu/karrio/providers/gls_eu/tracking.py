"""Karrio GLS EU tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.error as error
import karrio.providers.gls_eu.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable,
    settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    tracking_details = [
        _extract_details(event, settings) 
        for event in response.get("events", [])
    ]

    return tracking_details, messages


def _extract_details(data: dict, settings) -> models.TrackingDetails:
    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.get("trackingNumber", ""),
        events=[
            models.TrackingEvent(
                date=data.get("date"),
                description=data.get("description", ""),
                location=data.get("location", ""),
                code=data.get("statusCode", ""),
                time=data.get("time"),
            )
        ],
        delivered=data.get("status") == "DELIVERED",
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings,
) -> lib.Serializable:
    request = {
        "trackingNumbers": payload.tracking_numbers,
    }

    return lib.Serializable(request, lib.to_dict)
