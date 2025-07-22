import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, RatePayload, RateRequest, RateResponse

import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceAmericasRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = "{}"
            
            # Mock the OAuth call followed by rate call
            request = gateway.mapper.create_rate_request(self.RateRequest)
            response = gateway.proxy.get_rates(request)

            # Check OAuth call was made
            oauth_call = mock.call_args_list[0]
            self.assertIn("OAuth/AccessToken", oauth_call[1]["url"])
            
            # Check rate call was made
            rate_call = mock.call_args_list[1]
            self.assertEqual(
                rate_call[1]["url"],
                f"{gateway.settings.server_url}/rest/v2/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            
            request = gateway.mapper.create_rate_request(self.RateRequest)
            response = gateway.proxy.get_rates(request)
            parsed_response = gateway.mapper.parse_rate_response(response)

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


ParsedRateResponse = [
    [
        {
            "carrier_id": "dhl_ecommerce_americas",
            "carrier_name": "dhl_ecommerce_americas",
            "currency": "USD",
            "extra_charges": [
                {"amount": 10.0, "currency": "USD", "name": "Base Rate"},
                {"amount": 2.5, "currency": "USD", "name": "Fuel Surcharge"},
            ],
            "meta": {
                "delivery_guarantee": False,
                "product_code": "DHLParcelGround",
                "service_name": "DHL Parcel Ground",
            },
            "service": "DHLParcelGround",
            "total_charge": 12.5,
            "transit_days": 3,
        }
    ],
    [],
]
