"""ShipEngine carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestShipEngineTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["1Z999AA1234567890"],
    "reference": "ORDER123"
}

TrackingRequest = ["1Z999AA1234567890"]

TrackingResponse = """{
  "tracking_number": "1Z999AA1234567890",
  "status_code": "DE",
  "status_description": "Delivered",
  "carrier_code": "ups",
  "carrier_status_description": "Package delivered",
  "estimated_delivery_date": "2024-01-15T10:30:00Z",
  "actual_delivery_date": "2024-01-15T10:30:00Z",
  "tracking_url": "https://www.ups.com/track?tracknum=1Z999AA1234567890",
  "events": [
    {
      "occurred_at": "2024-01-15T10:30:00Z",
      "description": "Package delivered",
      "event_code": "DL",
      "city_locality": "Los Angeles",
      "state_province": "CA",
      "country_code": "US"
    },
    {
      "occurred_at": "2024-01-15T08:00:00Z",
      "description": "Out for delivery",
      "event_code": "OD",
      "city_locality": "Los Angeles", 
      "state_province": "CA",
      "country_code": "US"
    }
  ]
}"""

ErrorResponse = """{
  "errors": [
    {
      "error_code": "tracking_error",
      "message": "Unable to track shipment",
      "error_source": "shipengine",
      "error_type": "validation",
      "field_name": "tracking_number",
      "field_value": "Invalid tracking number"
    }
  ]
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "delivered": False,
            "estimated_delivery": "2024-01-15",
            "events": [
                {
                    "code": "DL",
                    "date": "2024-01-15",
                    "description": "Package delivered",
                    "location": "Los Angeles, CA, US",
                    "time": "10:30",
                    "timestamp": "2024-01-15T10:30:00.000Z",
                },
                {
                    "code": "OD",
                    "date": "2024-01-15",
                    "description": "Out for delivery",
                    "location": "Los Angeles, CA, US",
                    "time": "08:00",
                    "timestamp": "2024-01-15T08:00:00.000Z",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.ups.com/track?tracknum=1Z999AA1234567890",
                "expected_delivery": "2024-01-15",
                "source": "ups"
            },
            "meta": {
                "actual_delivery_date": "2024-01-15T10:30:00Z",
                "carrier_code": "ups",
                "carrier_status": "Package delivered",
                "status_code": "DE",
                "status_description": "Delivered"
            },
            "status": "in_transit",
            "tracking_number": "1Z999AA1234567890"
        }
    ],
    []
]

ParsedErrorResponse = [
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "delivered": False,
            "info": {},
            "meta": {},
            "status": "in_transit",
            "tracking_number": "1Z999AA1234567890"
        }
    ],
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "code": "tracking_error",
            "message": "Unable to track shipment",
            "details": {
                "error_source": "shipengine",
                "error_type": "validation",
                "field_name": "tracking_number",
                "field_value": "Invalid tracking number",
                "tracking_number": "1Z999AA1234567890"
            }
        }
    ]
]