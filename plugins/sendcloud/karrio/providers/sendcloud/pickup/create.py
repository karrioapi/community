"""Karrio Sendcloud pickup API implementation."""

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils
import karrio.providers.sendcloud.units as provider_units


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    pickup = lib.identity(
        _extract_details(response, settings)
        if response.get("label")
        else None
    )

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    label_info = data.get("label", {})
    
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=str(label_info.get("id", "")),
        pickup_date=lib.fdate(label_info.get("created_at")),
        meta=dict(
            label_id=label_info.get("id"),
            label_url=label_info.get("label_printer"),
            status=label_info.get("status"),
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)
    
    request = {
        "label": {
            "for_printer": True,
            "parcels": payload.shipment_identifiers,
        }
    }

    return lib.Serializable(request, lib.to_dict)
