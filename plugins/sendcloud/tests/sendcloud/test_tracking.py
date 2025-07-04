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
        self.assertEqual(lib.to_dict(request.serialize()), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking"
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

TrackingRequest = {
    "tracking_numbers": [
        "TRACK123"
    ],
    "reference": "ORDER123"
}

TrackingResponse = """<?xml version="1.0"?>
<tracking-response>
    <tracking-info>
        <tracking-number>TRACK123</tracking-number>
        <status>in_transit</status>
        <status-details>Package is in transit</status-details>
        <estimated-delivery>2024-04-15</estimated-delivery>
        <events>
            <event>
                <date>2024-04-12</date>
                <time>14:30:00</time>
                <code>PU</code>
                <description>Package picked up</description>
                <location>San Francisco, CA</location>
            </event>
        </events>
    </tracking-info>
</tracking-response>"""

ErrorResponse = """<?xml version="1.0"?>
<error-response>
    <e>
        <code>tracking_error</code>
        <message>Unable to track shipment</message>
        <details>Invalid tracking number</details>
    </e>
</error-response>"""

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "tracking_number": "TRACK123",
            "events": [
                {
                    "date": "2024-04-12",
                    "time": "14:30:00",
                    "code": "PU",
                    "description": "Package picked up",
                    "location": "San Francisco, CA"
                }
            ],
            "estimated_delivery": "2024-04-15",
            "status": "in_transit"
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