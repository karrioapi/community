"""Karrio ShipEngine provider imports."""
from karrio.providers.shipengine.utils import Settings
from karrio.providers.shipengine.rate import (
    parse_rate_response,
    rate_request,
)
from karrio.providers.shipengine.shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.shipengine.tracking import (
    parse_tracking_response,
    tracking_request,
)
from karrio.providers.shipengine.address import (
    parse_address_validation_response,
    address_validation_request,
)

# Placeholder functions for unsupported operations
def parse_shipment_cancel_response(response, settings):
    """Placeholder for cancel response parsing."""
    from karrio.core.models import ConfirmationDetails, Message
    return ConfirmationDetails(carrier_id=settings.carrier_id, carrier_name=settings.carrier_name, operation="cancel", success=True), []

def shipment_cancel_request(payload, settings):
    """Placeholder for cancel request."""
    from karrio.lib import Serializable
    return Serializable({"label_id": payload.shipment_identifier}, dict)