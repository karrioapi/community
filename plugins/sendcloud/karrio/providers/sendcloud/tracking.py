"""
SendCloud Tracking Provider - API v2/v3 JSON Implementation
"""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units
import karrio.schemas.sendcloud.tracking_request as sendcloud
import karrio.schemas.sendcloud.parcel_response as shipping


def parse_tracking_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    errors = error.parse_error_response(response, settings)
    tracking_details = _extract_details(response, settings) if "parcel" in response else []

    return tracking_details, errors


def _extract_details(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.List[models.TrackingDetails]:
    parcel = lib.to_object(shipping.Parcel, response.get("parcel"))
    
    if not parcel:
        return []
    
    tracking_number = parcel.tracking_number or str(parcel.id)
    
    events = []
    if parcel.status:
        events.append(
            models.TrackingEvent(
                code=str(parcel.status.id),
                description=parcel.status.message,
                date=parcel.date_updated,
            )
        )
    
    return [
        models.TrackingDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            tracking_number=tracking_number,
            events=events,
            delivered=parcel.status.message.lower() == "delivered" if parcel.status else False,
            info=models.TrackingInfo(
                carrier_tracking_link=getattr(parcel, "tracking_url", None),
                shipping_date=parcel.date_created,
                delivery_date=parcel.date_announced,
                package_weight=f"{parcel.weight} kg" if parcel.weight else None,
                package_dimensions=f"{parcel.length}x{parcel.width}x{parcel.height} cm"
                if all([parcel.length, parcel.width, parcel.height])
                else None,
            ),
            meta=dict(
                parcel_id=parcel.id,
                reference=parcel.reference,
                service_name=parcel.shipment.name if parcel.shipment else None,
            ),
        )
    ]


def tracking_request(payload: models.TrackingRequest, _) -> lib.Serializable:
    request = lib.Serializable(
        dict(tracking_number=payload.tracking_numbers[0] if payload.tracking_numbers else None),
        lib.to_dict,
    )
    
    return lib.Serializable(request, lib.to_dict)
