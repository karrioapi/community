"""MyDHL carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestMyDHLRating(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/express/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "company_name": "Shipper Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "person_name": "John Doe",
        "phone_number": "1234567890",
        "email": "john@example.com"
    },
    "recipient": {
        "company_name": "Recipient Company",
        "address_line1": "456 Oak Ave",
        "city": "Los Angeles",
        "postal_code": "90210",
        "country_code": "US",
        "person_name": "Jane Doe",
        "phone_number": "0987654321",
        "email": "jane@example.com"
    },
    "parcels": [
        {
            "height": 10.0,
            "length": 12.0,
            "width": 8.0,
            "weight": 5.0,
            "weight_unit": "LB",
            "dimension_unit": "IN"
        }
    ],
    "services": ["express_worldwide"],
    "options": {
        "currency": "USD"
    }
}

RateRequest = {
    "ClientDetail": ANY,
    "RequestedShipment": {
        "DropoffType": "REGULAR_PICKUP",
        "Shipper": ANY,
        "Recipient": ANY,
        "ShippingChargesPayment": ANY,
        "PackagingType": "YOUR_PACKAGING",
        "RequestedPackageLineItems": ANY
    }
}

RateResponse = """<RateResponse></RateResponse>"""

ParsedRateResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "currency": "USD",
        "service": "express_worldwide",
        "total_charge": 0.0,
        "transit_days": 1,
        "extra_charges": [],
        "meta": None
    }
] 
