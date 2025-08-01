"""Karrio GLS EU shipment cancel API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.error as error


def parse_shipment_cancel_response(
    _response: lib.Deserializable,
    settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    confirmation = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Cancel Shipment",
        success=True,
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings,
) -> lib.Serializable:
    """Create a shipment cancel request for the GLS EU API"""
    
    request = {
        "shipmentId": payload.shipment_identifier,
        "reason": "Customer request"
    }

    return lib.Serializable(request, lib.to_dict)
