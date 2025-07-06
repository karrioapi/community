"""ShipEngine carrier rate tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestShipEngineRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
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
        "company_name": "Test Company",
        "address_line1": "123 Test Street",
        "city": "Austin",
        "postal_code": "78701",
        "country_code": "US",
        "state_code": "TX",
        "person_name": "Test Shipper",
        "phone_number": "+1234567890",
        "email": "test@example.com"
    },
    "recipient": {
        "company_name": "Recipient Company",
        "address_line1": "456 Recipient St",
        "city": "Los Angeles",
        "postal_code": "90210",
        "country_code": "US",
        "state_code": "CA",
        "person_name": "Test Recipient",
        "phone_number": "+0987654321",
        "email": "recipient@example.com"
    },
    "parcels": [
        {
            "height": 10.0,
            "length": 12.0,
            "width": 8.0,
            "weight": 5.0,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "packaging_type": "package"
        }
    ]
}

RateRequest = {
    "rate_options": {
        "calculate_tax_amount": True,
        "preferred_currency": "USD"
    },
    "shipment": {
        "validate_address": "validate_and_clean",
        "ship_to": {
            "name": "Test Recipient",
            "phone": "+0987654321",
            "company_name": "Recipient Company",
            "address_line1": "456 Recipient St",
            "city_locality": "Los Angeles",
            "state_province": "CA",
            "postal_code": 90210,
            "country_code": "US",
            "address_residential_indicator": "no"
        },
        "ship_from": {
            "name": "Test Shipper",
            "phone": "+1234567890", 
            "company_name": "Test Company",
            "address_line1": "123 Test Street",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": 78701,
            "country_code": "US",
            "address_residential_indicator": "no"
        },
        "packages": [
            {
                "weight": {
                    "value": 5.0,
                    "unit": "pound"
                },
                "dimensions": {
                    "unit": "inch",
                    "length": 12.0,
                    "width": 8.0,
                    "height": 10.0
                },
                "package_code": "package"
            }
        ]
    }
}

RateResponse = """{
  "rate_response": {
    "rates": [
      {
        "rate_id": "se-123456789",
        "carrier_id": "se-test-carrier",
        "carrier_code": "ups",
        "service_code": "ups_ground",
        "service_type": "UPS Ground",
        "carrier_friendly_name": "UPS",
        "shipping_amount": {
          "amount": "12.50",
          "currency": "USD"
        },
        "insurance_amount": {
          "amount": "0.00",
          "currency": "USD"
        },
        "confirmation_amount": {
          "amount": "0.00", 
          "currency": "USD"
        },
        "other_amount": {
          "amount": "0.00",
          "currency": "USD"
        },
        "delivery_days": 3,
        "estimated_delivery_date": "2024-01-18T10:30:00Z",
        "guaranteed_service": false,
        "trackable": true
      },
      {
        "rate_id": "se-987654321",
        "carrier_id": "se-test-carrier-2",
        "carrier_code": "fedex",
        "service_code": "fedex_2day",
        "service_type": "FedEx 2Day",
        "carrier_friendly_name": "FedEx",
        "shipping_amount": {
          "amount": "25.99",
          "currency": "USD"
        },
        "insurance_amount": {
          "amount": "2.00",
          "currency": "USD"
        },
        "confirmation_amount": {
          "amount": "0.00",
          "currency": "USD"
        },
        "other_amount": {
          "amount": "1.50",
          "currency": "USD"
        },
        "delivery_days": 2,
        "estimated_delivery_date": "2024-01-16T10:30:00Z",
        "guaranteed_service": true,
        "trackable": true
      }
    ]
  }
}"""

ErrorResponse = """{
  "errors": [
    {
      "error_code": "rate_error",
      "message": "Unable to get rates",
      "error_source": "shipengine",
      "error_type": "validation",
      "field_name": "address",
      "field_value": "Invalid address information provided"
    }
  ]
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine", 
            "service": "shipengine_ups_ups_ground",
            "total_charge": 12.50,
            "currency": "USD",
            "transit_days": 3,
            "meta": {
                "service_name": "UPS Ground",
                "carrier_code": "ups",
                "carrier_name": "UPS",
                "rate_id": "se-123456789",
                "carrier_id": "se-test-carrier",
                "estimated_delivery_date": "2024-01-18T10:30:00Z",
                "guaranteed_service": False,
                "trackable": True
            }
        },
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "service": "shipengine_fedex_fedex_2day", 
            "total_charge": 29.49,
            "currency": "USD",
            "transit_days": 2,
            "meta": {
                "service_name": "FedEx 2Day",
                "carrier_code": "fedex",
                "carrier_name": "FedEx",
                "rate_id": "se-987654321",
                "carrier_id": "se-test-carrier-2",
                "estimated_delivery_date": "2024-01-16T10:30:00Z",
                "guaranteed_service": True,
                "trackable": True
            }
        }
    ],
    []
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "code": "rate_error",
            "message": "Unable to get rates",
            "details": {
                "error_source": "shipengine",
                "error_type": "validation",
                "field_name": "address",
                "field_value": "Invalid address information provided"
            }
        }
    ]
]