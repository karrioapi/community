import karrio.schemas.dhl_ecommerce_americas.tracking_response as dhl_tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    tracking_details = []
    if isinstance(response, dict):
        if "body" in response:
            tracking_details.append(_extract_details(response["body"], settings))
        elif "trackingNumber" in response:
            tracking_details.append(_extract_details(response, settings))

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    tracking_data = lib.to_object(dhl_tracking.Body, data)
    
    # Determine delivery status
    delivered = False
    status = "in_transit"
    
    if tracking_data.status:
        status_lower = tracking_data.status.lower()
        if status_lower in ["delivered", "delivered_to_recipient"]:
            delivered = True
            status = "delivered"
        elif status_lower in ["in_transit", "shipped"]:
            status = "in_transit"
        elif status_lower in ["out_for_delivery"]:
            status = "out_for_delivery"
        else:
            status = "in_transit"

    # Extract events
    events = []
    if tracking_data.events:
        for event_data in tracking_data.events:
            if isinstance(event_data, dict):
                event = lib.to_object(dhl_tracking.Event, event_data)
            else:
                event = event_data
                
            events.append(models.TrackingEvent(
                date=lib.fdate(event.eventDate, "%Y-%m-%d"),
                description=event.eventDescription or "No description",
                code=event.eventCode or "",
                time=lib.flocaltime(f"{event.eventDate}T{event.eventTime}", "%Y-%m-%dT%H:%M:%S"),
                location=event.location or "",
            ))

    # Parse delivery date
    estimated_delivery = None
    if tracking_data.deliveryDate:
        estimated_delivery = lib.fdate(tracking_data.deliveryDate, "%Y-%m-%d")

    # Safe tracking URL generation
    tracking_url = getattr(settings, 'tracking_url', None)
    carrier_tracking_link = None
    if tracking_url and tracking_data.trackingNumber:
        try:
            carrier_tracking_link = tracking_url.format(tracking_data.trackingNumber)
        except:
            carrier_tracking_link = f"https://track.dhl.com/tracking?lang=en&id={tracking_data.trackingNumber}"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_data.trackingNumber,
        status=status,
        delivered=delivered,
        estimated_delivery=estimated_delivery,
        events=events,
        info=models.TrackingInfo(
            carrier_tracking_link=carrier_tracking_link,
            signed_by=tracking_data.signedBy,
        ),
        meta=dict(
            delivery_date=tracking_data.deliveryDate,
            delivery_time=tracking_data.deliveryTime,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers
    return lib.Serializable(request)
