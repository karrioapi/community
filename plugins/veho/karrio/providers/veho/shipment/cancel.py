"""Karrio Veho shipment cancel API implementation."""

import karrio.schemas.veho.shipment_cancel_request as veho
import karrio.schemas.veho.shipment_cancel_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """
    Parse shipment cancellation response from carrier API

    _response: The carrier response to deserialize
    settings: The carrier connection settings

    Returns a tuple with (ConfirmationDetails, List[Message])
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    confirmation = _extract_details(response, settings) if "success" in response else None

    return confirmation, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ConfirmationDetails:
    """Extract cancellation confirmation details from carrier response data using typed objects."""
    # Convert to typed object
    cancel_response = lib.to_object(shipping.ShipmentCancelResponse, data)
    success = cancel_response.success or False
    
    return models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        operation="Cancel Shipment",
        success=success,
    )


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment cancellation request for the carrier API

    payload: The standardized ShipmentCancelRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    
    # Create JSON request for shipment cancellation
    # Example implementation:
    # import karrio.schemas.veho.shipment_cancel_request as veho_req
    #
    # request = veho_req.ShipmentCancelRequestType(
    #     shipmentId=payload.shipment_identifier,
    #     accountNumber=settings.account_number,
    #     # Add any other required fields
    # )
    #
    # return lib.Serializable(request, lib.to_dict)

    # For development, return a simple JSON request
    request = {
        "shipmentIdentifier": payload.shipment_identifier,
    }

    return lib.Serializable(request, lib.to_dict)
    
