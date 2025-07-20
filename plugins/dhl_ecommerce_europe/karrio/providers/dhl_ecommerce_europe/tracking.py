import karrio.schemas.dhl_ecommerce_europe.tracking_response as dhl_tracking
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
    shipment = lib.to_object(dhl_tracking.Shipment, data)
    
    # Determine delivery status - handle both dict and object status
    delivered = False
    status = "in_transit"
    
    if shipment.status:
        # Handle dict status
        if isinstance(shipment.status, dict):
            status_code = shipment.status.get("statusCode", "").lower()
        else:
            # Handle object status 
            status_code = getattr(shipment.status, 'statusCode', '').lower()
            
        if status_code in ["delivered", "ok"]:
            delivered = True
            status = "delivered"
        elif status_code in ["in_transit", "pu"]:
            status = "in_transit"
        else:
            status = "in_transit"

    # Extract events - handle both dict and object events
    events = []
    if shipment.events:
        for event_data in shipment.events:
            if isinstance(event_data, dict):
                event = lib.to_object(dhl_tracking.Event, event_data)
            else:
                event = event_data
                
            events.append(models.TrackingEvent(
                date=lib.fdate(event.timestamp, "%Y-%m-%dT%H:%M:%S"),
                description=event.description,
                code=event.typeCode,
                time=lib.flocaltime(event.timestamp, "%Y-%m-%dT%H:%M:%S"),
                location=f"{event.location.address.addressLocality}, {event.location.address.postalCode}, {event.location.address.countryCode}" if event.location and event.location.address else None,
            ))

    # Safe tracking URL generation
    tracking_url = getattr(settings, 'tracking_url', None)
    carrier_tracking_link = None
    if tracking_url and shipment.shipmentTrackingNumber:
        try:
            carrier_tracking_link = tracking_url.format(shipment.shipmentTrackingNumber)
        except:
            carrier_tracking_link = f"https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?lang=de&idc={shipment.shipmentTrackingNumber}"

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.shipmentTrackingNumber,
        status=status,
        delivered=delivered,
        estimated_delivery=lib.fdate(shipment.estimatedTimeOfDelivery, "%Y-%m-%dT%H:%M:%S") if shipment.estimatedTimeOfDelivery else None,
        events=events,
        info=models.TrackingInfo(
            carrier_tracking_link=carrier_tracking_link,
        ),
        meta=dict(
            shipment_status=shipment.status if isinstance(shipment.status, dict) else lib.to_dict(shipment.status),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = payload.tracking_numbers
    return lib.Serializable(request)
