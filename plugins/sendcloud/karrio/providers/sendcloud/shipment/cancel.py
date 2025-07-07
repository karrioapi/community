"""Karrio SendCloud shipment cancellation API implementation."""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendcloud.error as error
import karrio.providers.sendcloud.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from SendCloud API."""
    response = _response.deserialize()
    
    # Check for explicit success field first
    if response.get("success") is True:
        # This is a success response, don't parse as error
        confirmation = models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=True,
        )
        return confirmation, []
    
    # Otherwise, parse errors normally
    messages = error.parse_error_response(response, settings)
    success = len(messages) == 0

    # Create confirmation details if successful
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        ) if success else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment cancellation request for SendCloud API."""
    # SendCloud uses a simple POST to /parcels/{id}/cancel endpoint
    # The parcel ID should be in the shipment_identifier
    
    return lib.Serializable(
        dict(shipment_id=payload.shipment_identifier),
        lib.to_dict,
        ctx=dict(shipment_id=payload.shipment_identifier),
    )
    
