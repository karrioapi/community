import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_europe.error as error
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils
import karrio.providers.dhl_ecommerce_europe.units as provider_units


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    tracking_details = []
    if "shipments" in response:
        for shipment_data in response["shipments"]:
            tracking_details.append(_extract_details(shipment_data, settings))

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    shipment = data
    
    # Determine delivery status - handle both dict and object status
    delivered = False
    status = "in_transit"
    
    if data.status:
        # Handle dict status
        if isinstance(data.status, dict):
            status_code = data.status.get("statusCode", "").lower()
        else:
            # Handle object status 
            status_code = getattr(data.status, 'statusCode', '').lower()
            
        if status_code in ["delivered", "ok"]:
            delivered = True
            status = "delivered"
        elif status_code in ["in_transit", "pu"]:
            status = "in_transit"
        else:
            status = "in_transit"

    # Extract events - handle both dict and object events
    events = []
    if data.events:
        for event_data in data.events:
            if isinstance(event_data, dict):
                event = event_data
            else:
                event = event_data
                
            events.append(models.TrackingEvent(
                date=lib.fdate(event_data.timestamp, "%Y-%m-%dT%H:%M:%S"),
                description=event_data.description,
                code=event_data.typeCode,
                time=lib.flocaltime(event_data.timestamp, "%Y-%m-%dT%H:%M:%S"),
                location=f"{event_data.location.address.addressLocality}, {event_data.location.address.postalCode}, {event_data.location.address.countryCode}" if event_data.location and event_data.location.address else None,
            ))

    # Safe tracking URL generation
    tracking_url = getattr(settings, 'tracking_url', None)
    carrier_tracking_link = None
    if tracking_url and data.shipmentTrackingNumber:
        try:
            carrier_tracking_link = tracking_url.format(data.shipmentTrackingNumber)
        except:
            carrier_tracking_link = f"https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?lang=de&idc={data.shipmentTrackingNumber}"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data.shipmentTrackingNumber,
        status=status,
        delivered=delivered,
        estimated_delivery=lib.fdate(data.estimatedTimeOfDelivery, "%Y-%m-%dT%H:%M:%S") if data.estimatedTimeOfDelivery else None,
        events=events,
        info=models.TrackingInfo(
            carrier_tracking_link=carrier_tracking_link,
        ),
        meta=dict(
            shipment_status=data.status if isinstance(data.status, dict) else lib.to_dict(data.status),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers
    return lib.Serializable(request)
