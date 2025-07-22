import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, TrackingPayload, TrackingResponse

import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceAmericasTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = "{}"
            
            request = gateway.mapper.create_tracking_request(self.TrackingRequest)
            response = gateway.proxy.get_tracking(request)

            # Check OAuth call
            oauth_call = mock.call_args_list[0]
            self.assertIn("OAuth/AccessToken", oauth_call[1]["url"])
            
            # Check tracking call
            tracking_call = mock.call_args_list[1]
            self.assertEqual(
                tracking_call[1]["url"],
                f"{gateway.settings.server_url}/rest/v2/tracking/9374869903500938123456",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            
            request = gateway.mapper.create_tracking_request(self.TrackingRequest)
            response = gateway.proxy.get_tracking(request)
            parsed_response = gateway.mapper.parse_tracking_response(response)

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            
            request = gateway.mapper.create_tracking_request(self.TrackingRequest)
            response = gateway.proxy.get_tracking(request)
            parsed_response = gateway.mapper.parse_tracking_response(response)

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingRequest = ["9374869903500938123456"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_ecommerce_americas",
            "carrier_name": "dhl_ecommerce_americas",
            "delivered": False,
            "estimated_delivery": "2025-01-23",
            "events": [
                {
                    "code": "PU",
                    "date": "2025-01-20",
                    "description": "Package picked up",
                    "location": "New York, NY",
                    "time": "10:30",
                },
                {
                    "code": "OFD",
                    "date": "2025-01-22",
                    "description": "Out for delivery",
                    "location": "Los Angeles, CA",
                    "time": "14:45",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.dhl.com/tracking?lang=en&id=9374869903500938123456",
                "signed_by": None,
            },
            "meta": {
                "delivery_date": "2025-01-23",
                "delivery_time": "16:30:00",
            },
            "status": "in_transit",
            "tracking_number": "9374869903500938123456",
        }
    ],
    [],
]

ErrorResponse = """{
  "header": {
    "code": 400,
    "message": "Bad Request",
    "messageDetail": "Invalid tracking number format"
  },
  "body": {
    "errors": [
      {
        "errorCode": "INVALID_TRACKING_NUMBER",
        "errorMessage": "The tracking number format is invalid",
        "errorDescription": "Tracking number must be 22 digits"
      }
    ]
  }
}"""

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dhl_ecommerce_americas",
            "carrier_name": "dhl_ecommerce_americas",
            "code": "400",
            "details": {"messageDetail": "Invalid tracking number format"},
            "message": "Bad Request",
        }
    ],
]
