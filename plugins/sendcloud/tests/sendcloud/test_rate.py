"""SendCloud carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestSendCloudRating(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "parcels": [{
        "weight": 10.0,
        "width": 10.0,
        "height": 10.0,
        "length": 10.0,
        "weight_unit": "KG",
        "dimension_unit": "CM",
        "packaging_type": "BOX"
    }]
}

RateRequest = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Person",
        "company_name": "Test Company",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weight_unit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimension_unit": "CM",
            "packaging_type": "BOX"
        }
    ]
}

RateResponse = """{
  "rates": [
    {
      "service_code": "express",
      "service_name": "Express Service",
      "total_charge": 25.99,
      "currency": "USD",
      "transit_days": 2
    },
    {
      "service_code": "ground",
      "service_name": "Ground Service",
      "total_charge": 12.99,
      "currency": "USD",
      "transit_days": 5
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "rate_error",
    "message": "Unable to get rates",
    "details": "Invalid address provided"
  }
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "service": "express",
            "currency": "USD",
            "total_charge": 25.99,
            "transit_days": 2,
            "meta": {
                "service_name": "Express Service"
            }
        },
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "service": "ground",
            "currency": "USD",
            "total_charge": 12.99,
            "transit_days": 5,
            "meta": {
                "service_name": "Ground Service"
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
            "code": "rate_error",
            "message": "Unable to get rates",
            "details": {
                "details": "Invalid address provided"
            }
        }
    ]
]
