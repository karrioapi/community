"""SendCloud carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSendCloudTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking/TRACK123"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["TRACK123"],
    "reference": "ORDER123"
}

TrackingRequest = [
    {
        "tracking_number": "TRACK123",
        "carrier": None
    }
]

TrackingResponse = """{
  "parcel": {
    "id": 12345,
    "tracking_number": "TRACK123",
    "status": {
      "id": 5,
      "message": "In Transit"
    },
    "tracking_events": [
      {
        "timestamp": "2024-04-12T14:30:00",
        "status": "PU",
        "message": "Package picked up",
        "location": {
          "city": "San Francisco",
          "country": "US"
        }
      }
    ],
    "tracking_url": "https://tracking.sendcloud.sc/TRACK123",
    "weight": "1.5",
    "carrier": {
      "code": "postnl",
      "name": "PostNL"
    },
    "shipment": {
      "id": 54321,
      "name": "EXPRESS"
    }
  }
}"""

ErrorResponse = """{
  "error": {
    "code": "tracking_error",
    "message": "Unable to track shipment",
    "details": "Invalid tracking number"
  }
}"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "tracking_number": "TRACK123",
            "events": [
                {
                    "date": "2024-04-12",
                    "time": "14:30",
                    "code": "PU",
                    "description": "Package picked up",
                    "location": "San Francisco, US"
                }
            ],
            "delivered": False,
            "status": "in_transit",
            "info": {
                "carrier_tracking_link": "https://tracking.sendcloud.sc/TRACK123",
                "shipment_package_count": 1,
                "package_weight": 1.5,
                "package_weight_unit": "KG"
            },
            "meta": {
                "sendcloud_parcel_id": 12345,
                "sendcloud_status_id": 5,
                "sendcloud_status_message": "In Transit",
                "carrier_code": "postnl",
                "carrier_name": "PostNL",
                "shipment_id": 54321,
                "shipment_name": "EXPRESS"
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "code": "tracking_error",
            "message": "Unable to track shipment",
            "details": {
                "details": "Invalid tracking number"
            }
        }
    ]
]