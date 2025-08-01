from typing import List, Tuple
from karrio.core.utils import Deserializable, DF, SF
from karrio.core.models import (
    TrackingRequest,
    TrackingDetails,
    TrackingEvent,
    Message,
)
from karrio.providers.dhl_express.error import parse_error_response
from karrio.providers.dhl_express.utils import Settings, request
import karrio.providers.dhl_express.units as provider_units
import karrio.lib as lib


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: Settings,
) -> Tuple[List[TrackingDetails], List[Message]]:
    response = _response.deserialize()
    messages: List[Message] = parse_error_response(response, settings)
    tracking_details: List[TrackingDetails] = []

    if "shipments" in response:
        tracking_details = [
            _extract_details(shipment, settings)
            for shipment in response["shipments"]
        ]

    return tracking_details, messages


def _extract_details(
    shipment_data: dict,
    settings: Settings,
) -> TrackingDetails:
    events = []
    shipment_events = shipment_data.get("events", [])
    
    if shipment_events:
        for event_data in shipment_events:
            if isinstance(event_data, dict):
                location = None
                if event_data.get("location") and event_data["location"].get("address"):
                    addr = event_data["location"]["address"]
                    location = f"{addr.get('addressLocality', '')}, {addr.get('postalCode', '')}, {addr.get('countryCode', '')}"
                
                events.append(
                    TrackingEvent(
                        code=event_data.get("typeCode"),
                        description=event_data.get("description"),
                        date=lib.fdate(event_data.get("timestamp"), "%Y-%m-%dT%H:%M:%S"),
                        time=lib.ftime(event_data.get("timestamp"), "%Y-%m-%dT%H:%M:%S", "%H:%M:%S"),
                        location=location,
                    )
                )

    status = "in_transit"  # default
    shipment_status = shipment_data.get("status")
    if shipment_status:
        if isinstance(shipment_status, dict):
            status_code = shipment_status.get("statusCode")
        else:
            status_code = str(shipment_status)
        status = _extract_status(status_code)

    return TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment_data.get("shipmentTrackingNumber"),
        events=events,
        status=status,
        delivered=status == "delivered",
        estimated_delivery=lib.fdate(
            shipment_data.get("estimatedTimeOfDelivery"), "%Y-%m-%dT%H:%M:%S"
        ) if shipment_data.get("estimatedTimeOfDelivery") else None,
        meta=dict(
            shipment_status=shipment_status,
        ),
    )


def _extract_status(status_code: str) -> str:
    """Extract unified status from DHL Express status code."""
    if not status_code:
        return "in_transit"
    
    status_code = status_code.upper()
    
    if status_code in ["DELIVERED", "OK"]:
        return "delivered"
    elif status_code in ["TRANSIT", "PICKED_UP", "PU"]:
        return "in_transit"
    elif status_code in ["DELAYED"]:
        return "delivery_delayed"
    elif status_code in ["FAILED", "EXCEPTION"]:
        return "delivery_failed"
    elif status_code in ["HOLD"]:
        return "on_hold"
    else:
        return "in_transit"


def get_tracking(payload: TrackingRequest, settings: Settings) -> Deserializable[str]:
    """Get tracking information from DHL Express."""
    
    tracking_numbers = ",".join(payload.tracking_numbers)
    response = request(
        url=f"{settings.server_url}/track/shipments?trackingNumber={tracking_numbers}",
        trace=payload.tracking_numbers,
        method="GET",
        settings=settings,
    )
    
    return Deserializable(response, lib.to_dict)
