"""Karrio GLS EU pickup cancel API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.error as error


def parse_pickup_cancel_response(
    _response: lib.Deserializable,
    settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    confirmation = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Cancel Pickup",
        success=True,
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings,
) -> lib.Serializable:
    request = {
        "pickupId": payload.confirmation_number,
        "reason": "Customer request"
    }

    return lib.Serializable(request, lib.to_dict)
