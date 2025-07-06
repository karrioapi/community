"""Karrio ShipEngine tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units
import karrio.schemas.shipengine.tracking_request as shipengine_req
import karrio.schemas.shipengine.tracking_response as shipengine_res


def parse_tracking_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=tracking_number)
            for tracking_number, response in responses
        ],
        start=[],
    )

    tracking_details = [
        _extract_details(details, settings, tracking_number)
        for tracking_number, details in responses
        if details and str(details).strip()
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    tracking_details = lib.to_object(shipengine_res.TrackingResponseType, data)
    
    tracking_number = tracking_number or tracking_details.tracking_number or ""
    
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.occurred_at, "%Y-%m-%dT%H:%M:%SZ") if event.occurred_at else None,
            description=event.description or '',
            code=event.event_code or '',
            time=lib.ftime(event.occurred_at, "%Y-%m-%dT%H:%M:%SZ") if event.occurred_at else None,
            location=", ".join(filter(None, [
                event.city_locality,
                event.state_province,
                event.country_code
            ])),
        )
        for event in (tracking_details.events or [])
    ]

    status = next(
        (
            status.name
            for status in list(provider_units.TrackingStatus)
            if tracking_details.status_code in status.value
        ),
        "in_transit",
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        events=events,
        estimated_delivery=lib.fdate(tracking_details.estimated_delivery_date, "%Y-%m-%dT%H:%M:%SZ") if tracking_details.estimated_delivery_date else None,
        delivered=status == "delivered",
        status=status,
        info=models.TrackingInfo(
            carrier_tracking_link=tracking_details.tracking_url,
            expected_delivery=lib.fdate(tracking_details.estimated_delivery_date, "%Y-%m-%dT%H:%M:%SZ") if tracking_details.estimated_delivery_date else None,
            source=tracking_details.carrier_code,
        ),
        meta=dict(
            carrier_code=tracking_details.carrier_code,
            carrier_status=tracking_details.carrier_status_description,
            status_code=tracking_details.status_code,
            status_description=tracking_details.status_description,
            actual_delivery_date=tracking_details.actual_delivery_date,
        ),
    )




def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create tracking requests for ShipEngine API."""

    # ShipEngine tracking uses simple tracking number list
    # No generated schema needed for this simple request
    return lib.Serializable(payload.tracking_numbers, lib.to_dict)
