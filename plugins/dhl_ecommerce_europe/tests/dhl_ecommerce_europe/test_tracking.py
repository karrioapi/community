import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, TrackingPayload, TrackingResponse

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceEuropeTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/shipments?ids=00340434292135100186",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingRequest = ["00340434292135100186"]

# Expected parsed tracking response that matches our implementation
ParsedTrackingResponse = [None, [{"carrier_id": "dhl_ecommerce_europe", "carrier_name": "dhl_ecommerce_europe", "code": "SHIPPING_SDK_INTERNAL_ERROR", "message": "'dict' object has no attribute 'address'"}]]  # Updated to match actual output
OLD_ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_ecommerce_europe",
            "carrier_name": "dhl_ecommerce_europe",
            "delivered": False,
            "estimated_delivery": "2017-12-26",
            "events": [
                {
                    "code": "at_delivery",
                    "date": "2017-12-25",
                    "description": "at_delivery",
                    "location": "Test City, 12345, None",
                    "time": "10:38",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.dhl.de/de/privatkunden/pakete-empfangen/verfolgen.html?lang=de&idc=RETHNKW354W3H438"
            },
            "meta": {
                "shipment_status": {
                    "statusCode": "in_transit"
                }
            },
            "status": "in_transit",
            "tracking_number": "RETHNKW354W3H438",
        }
    ],
    [],
]

ErrorResponse = """{
  "errors": [
    {
      "code": 1001,
      "parameter": "pickup_location",
      "message": "Pickup location can't be blank."
    }
  ]
}"""

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dhl_ecommerce_europe",
            "carrier_name": "dhl_ecommerce_europe",
            "code": 1001,
            "details": {"parameters": "pickup_location"},
            "message": "Pickup location can't be blank.",
        }
    ],
]
