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
        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/fetch-shipping-options"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed error response: {lib.to_dict(parsed_response)}")
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
    "fromcountry": "US",
    "tocountry": "US", 
    "frompostalcode": "12345",
    "topostalcode": "12345",
    "weight": 10.0,
    "length": 10,
    "width": 10,
    "height": 10,
    "isreturn": False,
    "requestlabelasync": False
}

RateResponse = """{
  "data": [
    {
      "code": "postnl:small/home_address_only,signature",
      "name": "PostNL Klein Pakket - 10 liter - Alleen Huisadres + Handtekening",
      "carrier": {
        "code": "postnl",
        "name": "PostNL"
      },
      "product": {
        "code": "postnl:small",
        "name": "PostNL Klein Pakket"
      },
      "functionalities": {
        "signature": true,
        "tracked": true,
        "age_check": null,
        "delivery_deadline": "best_effort",
        "weekend_delivery": null,
        "insurance": null
      },
      "contract": {
        "id": 60
      },
      "weight": {
        "min": {
          "value": "0.001",
          "unit": "kg"
        },
        "max": {
          "value": "23.001",
          "unit": "kg"
        }
      },
      "quotes": [
        {
          "price": {
            "total": {
              "value": "0",
              "currency": "EUR"
            },
            "breakdown": []
          },
          "lead_time": 24
        }
      ]
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "invalid_request",
    "message": "Unable to get shipping options",
    "details": "Invalid destination address provided"
  }
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "service": "sendcloud_postnl_postnl:small",
            "currency": "EUR",
            "total_charge": 0.0,
            "meta": {
                "carrier_code": "postnl",
                "contract_id": 60,
                "insurance_available": False,
                "max_weight": "23.001",
                "min_weight": "0.001",
                "product_code": "postnl:small",
                "rate_provider": "PostNL",
                "sendcloud_code": "postnl:small/home_address_only,signature",
                "service_name": "PostNL Klein Pakket - 10 liter - Alleen Huisadres + Handtekening",
                "signature": True,
                "tracked": True,
                "weight_unit": "kg"
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
            "code": "invalid_request",
            "details": {
                "details": "Invalid destination address provided"
            },
            "message": "Unable to get shipping options"
        }
    ]
]