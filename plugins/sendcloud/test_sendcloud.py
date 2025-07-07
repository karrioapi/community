#!/usr/bin/env python
"""Quick test script for SendCloud integration"""

import unittest
from unittest.mock import patch
import karrio.api.gateway
import karrio.mappers.sendcloud as sendcloud
import karrio.lib as lib
import karrio.core.models as models

# Create gateway directly
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

# Test data
RatePayload = {
    "shipper": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
    },
    "recipient": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
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

class TestSendCloudIntegration(unittest.TestCase):
    def test_create_rate_request(self):
        rate_request = models.RateRequest(**RatePayload)
        request = gateway.mapper.create_rate_request(rate_request)
        result = lib.to_dict(request.serialize())
        
        print("Rate request created:")
        print(f"  URL params: {result}")
        self.assertIn("fromcountry", result)
        self.assertIn("tocountry", result)
        self.assertEqual(result["weight"], 10.0)

    def test_parse_rate_response(self):
        import karrio.providers.sendcloud.rate as rate_module
        import karrio.lib as lib
        
        # Parse the response directly
        response = lib.Deserializable(RateResponse, lib.to_dict)
        rates, messages = rate_module.parse_rate_response(response, settings)
        
        print("Rate response parsed:")
        print(f"  Rates: {len(rates)}")
        if rates:
            rate = rates[0]
            print(f"  Service: {rate.service}")
            print(f"  Carrier: {rate.carrier_name}")
            print(f"  Total: {rate.total_charge} {rate.currency}")
            print(f"  Transit: {rate.transit_days}")
            print(f"  Meta keys: {list(rate.meta.keys())}")
        
        self.assertTrue(len(rates) > 0)
        rate = rates[0]
        self.assertEqual(rate.service, "sendcloud_postnl_postnl:small")
        self.assertEqual(rate.currency, "EUR")
        self.assertEqual(rate.transit_days, 24)

    def test_parse_error_response(self):
        import karrio.providers.sendcloud.error as error_module
        import karrio.lib as lib
        
        # Parse error response directly
        response_dict = lib.to_dict(lib.Deserializable(ErrorResponse, lib.to_dict).deserialize())
        messages = error_module.parse_error_response(response_dict, settings)
        
        print("Error response parsed:")
        print(f"  Messages: {len(messages)}")
        if messages:
            msg = messages[0]
            print(f"  Code: {msg.code}")
            print(f"  Message: {msg.message}")
            print(f"  Details: {msg.details}")
        
        self.assertTrue(len(messages) > 0)
        msg = messages[0]
        self.assertEqual(msg.code, "invalid_request")
        self.assertEqual(msg.message, "Unable to get shipping options")

if __name__ == "__main__":
    unittest.main(verbosity=2)