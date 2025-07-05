# SendCloud API v2/v3 JSON Schemas
from .parcel_request import (
    ParcelRequest,
    ParcelData,
    ParcelItem,
    Shipment,
)

from .parcel_response import (
    ParcelResponse,
    Parcel,
    ParcelItemResponse,
    Country,
    Status,
    Carrier,
    Label,
    AddressDivided,
    Document,
    ErrorResponse,
)

from .tracking_request import (
    TrackingRequest,
)

from .error_response import (
    ErrorDetail,
)

# Aliases for backward compatibility with provider files
shipment_request = ParcelRequest
shipment_response = ParcelResponse
rate_request = ParcelRequest  # Same structure for rate requests
rate_response = ParcelResponse  # Rate info comes in parcel response
tracking_request = TrackingRequest
tracking_response = ParcelResponse
