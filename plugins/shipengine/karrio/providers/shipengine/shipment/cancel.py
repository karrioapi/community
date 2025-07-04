"""Karrio ShipEngine shipment cancellation parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils


def parse_cancel_shipment_response(
    response: lib.Deserializable[typing.Dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    responses = lib.to_dict(response.deserialize())
    messages = error.parse_error_response(response, settings)
    
    # ShipEngine label void returns a successful response or error
    success = response.status_code == 200 or "approved" in str(responses).lower()
    
    confirmation: models.ConfirmationDetails = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Shipment Cancellation",
        success=success,
    )
    
    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # For ShipEngine, we need the label_id to void a label
    # This is typically passed via the shipment_identifier or label_id
    request = dict(
        shipengine_label_id=payload.shipment_identifier,
    )
    
    return lib.Serializable(request) 
