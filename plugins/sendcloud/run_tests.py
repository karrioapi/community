#!/usr/bin/env python
"""Run SendCloud tests without SDK dependency"""

import os
import sys

# Change to project directory
os.chdir('/Users/danielkobina/Workspace/karrio/patch/community/plugins/sendcloud')

# Test with standard pattern
import unittest
from unittest.mock import patch, ANY
import karrio.api.gateway
import karrio.mappers.sendcloud as sendcloud
import karrio.lib as lib
import karrio.core.models as models

# Create gateway
settings = sendcloud.Settings(
    client_id="test_client_id",
    client_secret="test_client_secret",
)

gateway = karrio.api.gateway.Gateway(
    mapper=sendcloud.Mapper(settings),
    proxy=sendcloud.Proxy(settings),
    settings=settings,
    is_hub=True,
    tracer=lambda: None,
)

# Test data from the real test file
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
        "agecheck": null,
        "deliverydeadline": "best_effort",
        "weekenddelivery": null,
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
          "leadtime": 24
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
            "transit_days": 24,
            "meta": {
                "carrier_code": "postnl",
                "contract_id": 60,
                "delivery_deadline": "best_effort",
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

class TestSendCloudRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        result = request.serialize()
        print(f"✓ Request created: {result}")
        self.assertEqual(result, RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            # This would normally use karrio.Rating.fetch but we'll just test the URL
            gateway.proxy.get_rates(gateway.mapper.create_rate_request(self.RateRequest))
            print(f"✓ Endpoint called: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/fetch-shipping-options"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            
            # Parse response directly
            response = lib.Deserializable(RateResponse, lib.to_dict)
            rates, messages = gateway.mapper.parse_rate_response(response)
            
            # Test with full structure comparison like the real tests
            parsed_response = [rates, messages]
            result = lib.to_dict(parsed_response)
            
            print(f"✓ Rate response parsed: {len(rates)} rates, {len(messages)} messages")
            print(f"Expected: {ParsedRateResponse}")
            print(f"Actual: {result}")
            
            # Use assertListEqual like the real tests
            self.assertListEqual(result, ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            
            # Parse error directly
            response = lib.Deserializable(ErrorResponse, lib.to_dict)
            rates, messages = gateway.mapper.parse_rate_response(response)
            
            # Test with full structure comparison
            parsed_response = [rates, messages]
            result = lib.to_dict(parsed_response)
            
            print(f"✓ Error response parsed: {len(rates)} rates, {len(messages)} messages")
            print(f"Expected: {ParsedErrorResponse}")
            print(f"Actual: {result}")
            
            # Use assertListEqual like the real tests
            self.assertListEqual(result, ParsedErrorResponse)

if __name__ == "__main__":
    print("🧪 Running SendCloud Integration Tests")
    print("=" * 50)
    unittest.main(verbosity=2)