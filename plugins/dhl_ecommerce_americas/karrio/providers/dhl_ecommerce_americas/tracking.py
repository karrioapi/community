"""Karrio DHL eCommerce Americas tracking API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_americas.error as error
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils
import karrio.providers.dhl_ecommerce_americas.units as provider_units
import karrio.schemas.dhl_ecommerce_americas.tracking_response as dhl_res

def parse_tracking_response(
    _response: lib.Deserializable,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    tracking_details = []
    for tracking_number, tracking_data in response:
        if not tracking_data:
            continue

        # Convert to typed object using generated schema
        tracking_response = lib.to_object(dhl_res.TrackingResponseType, tracking_data)
        
        if tracking_response.body:
            detail = _extract_details(lib.to_dict(tracking_response.body), settings, tracking_number)
            tracking_details.append(detail)

    return tracking_details, []

def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    tracking_number: str = None,
) -> models.TrackingDetails:
    """Extract tracking details from DHL response data"""

    # Convert the DHL data to a proper object for easy attribute access
    tracking_data = lib.to_object(dhl_res.TrackingResponseBodyType, data)

    # Use TrackingStatus enum for proper status mapping
    status = provider_units.TrackingStatus.map(tracking_data.status or "IN_TRANSIT")
    delivered = status == provider_units.TrackingStatus.delivered.value

    # Functional event processing with proper error handling
    events = [
        models.TrackingEvent(
            date=lib.fdate(event.eventDate, "%Y-%m-%d") if hasattr(event, 'eventDate') and event.eventDate else None,
            description=event.eventDescription if hasattr(event, 'eventDescription') else "No description",
            code=event.eventCode if hasattr(event, 'eventCode') else "",
            time=lib.flocaltime(
                f"{event.eventDate}T{event.eventTime}",
                "%Y-%m-%dT%H:%M:%S"
            ) if all([
                hasattr(event, 'eventDate'),
                hasattr(event, 'eventTime'),
                event.eventDate,
                event.eventTime
            ]) else None,
            location=event.location if hasattr(event, 'location') else "",
        )
        for event in (tracking_data.events or [])
    ]

    # Safe delivery date parsing
    estimated_delivery = (
        lib.fdate(tracking_data.deliveryDate, "%Y-%m-%d")
        if hasattr(tracking_data, 'deliveryDate') and tracking_data.deliveryDate
        else None
    )

    # Build tracking link
    tracking_number_to_use = tracking_number or (
        tracking_data.trackingNumber if hasattr(tracking_data, 'trackingNumber') else ""
    )
    
    carrier_tracking_link = (
        f"https://track.dhl.com/tracking?lang=en&id={tracking_number_to_use}"
        if tracking_number_to_use
        else None
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number_to_use,
        status=status,
        delivered=delivered,
        estimated_delivery=estimated_delivery,
        events=events,
        info=models.TrackingInfo(
            carrier_tracking_link=carrier_tracking_link,
            signed_by=tracking_data.signedBy if hasattr(tracking_data, 'signedBy') else None,
        ),
        meta=dict(
            delivery_date=tracking_data.deliveryDate if hasattr(tracking_data, 'deliveryDate') else None,
            delivery_time=tracking_data.deliveryTime if hasattr(tracking_data, 'deliveryTime') else None,
        ),
    )

def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a tracking request object."""
    return lib.Serializable(payload.tracking_numbers)