"""Karrio ShipEngine shipment cancellation API implementation."""
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
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

    # Extract success state from the response
    success = _extract_cancellation_status(response)

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


def _extract_cancellation_status(
    response: lib.Element
) -> bool:
    """
    Extract cancellation success status from the carrier response

    response: The deserialized carrier response

    Returns True if cancellation was successful, False otherwise
    """
    
    # Example implementation for XML response:
    # status_node = lib.find_element("shipment-status", response, first=True)
    # return status_node is not None and status_node.text.lower() == "cancelled"

    # For development, always return success
    return True
    


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
    
    # Create XML request for shipment cancellation
    # Example implementation:
    # import karrio.schemas.shipengine.shipment_cancel_request as shipengine_req
    #
    # request = shipengine_req.ShipmentCancelRequest(
    #     AccountNumber=settings.account_number,
    #     ShipmentReference=payload.shipment_identifier,
    #     # Add any other required fields
    # )
    #
    # return lib.Serializable(
    #     request,
    #     lambda _: lib.to_xml(
    #         _,
    #         name_="ShipmentCancelRequest",
    #         namespacedef_=(
    #             'xmlns="http://shipengine.com/schema/shipment/cancel"'
    #         ),
    #     )
    # )

    # For development, return a simple XML request
    request = f"""<?xml version="1.0"?>
<shipment-cancel-request>
  <shipment-reference>{payload.shipment_identifier}</shipment-reference>
</shipment-cancel-request>"""

    return lib.Serializable(request, lambda r: r)
    
