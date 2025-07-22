import unittest
from unittest.mock import patch, Mock
import karrio.core.models as models
import karrio.sdk as karrio
from karrio.mappers.dhl_express.settings import Settings
from tests.dhl_express.fixture import gateway, RatePayload, RateResponse


class TestDHLExpressRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    @patch("karrio.mappers.dhl_express.proxy.lib.request")
    def test_get_rate(self, mock_request):
        mock_request.return_value = RateResponse
        rates, messages = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
        
        self.assertEqual(
            mock_request.call_args[1]["url"],
            f"{gateway.settings.server_url}/rates",
        )
        self.assertEqual(len(rates), 1)
        self.assertEqual(rates[0].service, "DHL Express Worldwide")
        self.assertEqual(float(rates[0].total_charge), 45.50)
        self.assertEqual(rates[0].currency, "USD")

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        
        # Check if the request structure is correct
        request_data = request.serialize()
        self.assertIn("plannedShippingDateAndTime", request_data)
        self.assertIn("customerDetails", request_data)
        self.assertIn("packages", request_data)

    def test_parse_rate_response(self):
        parsed_response = gateway.mapper.parse_rate_response(
            Mock(deserialize=lambda: RateResponse)
        )
        rates, messages = parsed_response
        
        self.assertEqual(len(rates), 1)
        self.assertEqual(rates[0].service, "DHL Express Worldwide")
        self.assertEqual(float(rates[0].total_charge), 45.50)


if __name__ == "__main__":
    unittest.main()
