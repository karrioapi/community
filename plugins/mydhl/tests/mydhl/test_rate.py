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
        print(f"Generated request: {lib.to_dict(request.serialize())}")  # MANDATORY DEBUG PRINT
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")  # MANDATORY DEBUG PRINT
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mydhlapi/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
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
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "addressLine1": "123 Test Street",
        "city": "Test City",
        "postalCode": "12345",
        "countryCode": "US",
        "stateCode": "CA",
        "personName": "Test Person",
        "companyName": "Test Company",
        "phoneNumber": "1234567890",
        "email": "test@example.com"
    },
    "packages": [
        {
            "weight": 10.0,
            "weightUnit": "KG",
            "length": 10.0,
            "width": 10.0,
            "height": 10.0,
            "dimensionUnit": "CM",
            "packagingType": "BOX"
        }
    ]
}

RateResponse = """{
  "products": [
    {
      "productName": "EXPRESS WORLDWIDE",
      "productCode": "U",
      "totalPrice": [
        {
          "currencyType": "BILLC",
          "priceCurrency": "USD",
          "price": 25.99
        }
      ],
      "deliveryCapabilities": {
        "totalTransitDays": 2,
        "estimatedDeliveryDateAndTime": "2019-09-20T12:00:00"
      },
      "pickupCapabilities": {
        "localCutoffDateAndTime": "2019-09-18T15:00:00"
      }
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
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "service": "U",
            "currency": "USD",
            "total_charge": 25.99,
            "transit_days": 2,
            "meta": {
                "service_name": "EXPRESS WORLDWIDE",
                "delivery_time": "2019-09-20T12:00:00",
                "pickup_cutoff": "2019-09-18T15:00:00"
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "rate_error",
            "message": "Unable to get rates",
            "details": {
                "details": "Invalid address provided"
            }
        }
    ]
]