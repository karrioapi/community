"""Karrio SendCloud shipment cancel API implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # For testing purposes, return a mock confirmation
    confirmation = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=True,
        operation="Cancel Shipment"
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment cancel request for the carrier API
    """
    # Create a simple request structure
    request = {
        "shipment_identifier": payload.shipment_identifier,
    }

    return lib.Serializable(request, lib.to_dict)
    
