"""Karrio Amazon Shipping shipment cancellation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.amazon_shipping.error as error
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from Amazon Shipping API.

    The v2 cancelShipment API returns an empty response on success
    or an error object on failure.
    """
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Success if no errors returned
    success = len(messages) == 0

    details = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=success,
        operation="Cancel Shipment",
    ) if success else None

    return details, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create Amazon Shipping shipment cancellation request.

    Returns the shipment ID to be used in the cancel API path.
    """
    return lib.Serializable(payload.shipment_identifier)
