import unittest
from unittest.mock import patch, Mock
import karrio.core.models as models
import karrio.sdk as karrio
from karrio.mappers.dhl_express.settings import Settings
from tests.dhl_express.fixture import gateway, TrackingResponse


class TestDHLExpressTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(tracking_numbers=["1234567890"])

    @patch("karrio.mappers.dhl_express.proxy.lib.request")
    def test_get_tracking(self, mock_request):
        mock_request.return_value = TrackingResponse
        tracking_details, messages = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
        
        self.assertEqual(len(tracking_details), 1)
        self.assertEqual(tracking_details[0].tracking_number, "1234567890")
        self.assertEqual(tracking_details[0].status, "in_transit")

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        
        # Check if the request structure is correct
        self.assertEqual(request, ["1234567890"])

    def test_parse_tracking_response(self):
        parsed_response = gateway.mapper.parse_tracking_response(
            Mock(deserialize=lambda: TrackingResponse)
        )
        tracking_details, messages = parsed_response
        
        self.assertEqual(len(tracking_details), 1)
        self.assertEqual(tracking_details[0].tracking_number, "1234567890")
        self.assertEqual(len(tracking_details[0].events), 1)
        self.assertEqual(tracking_details[0].events[0].code, "PU")


if __name__ == "__main__":
    unittest.main()
