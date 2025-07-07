"""MyDHL carrier address validation tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class TestMyDHLAddress(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")  # MANDATORY DEBUG PRINT
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")  # MANDATORY DEBUG PRINT
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mydhlapi/address-validate"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {
    "address": {
        "address_line1": "123 Main St",
        "city": "City Name",
        "postal_code": "12345",
        "country_code": "US",
        "state_code": "CA",
    }
}

AddressValidationRequest = {
  "type": "delivery",
  "countryCode": "US",
  "postalCode": "12345",
  "cityName": "City Name",
  "strictValidation": True
}

AddressValidationResponse = """{
  "warnings": [],
  "address": [
    {
      "countryCode": "US",
      "postalCode": "12345",
      "cityName": "City Name",
      "serviceArea": {
        "code": "NYC",
        "description": "New York Service Area",
        "GMTOffset": "-05:00"
      }
    }
  ]
}"""

ErrorResponse = """{
  "error": {
    "code": "address_error",
    "message": "Unable to validate address",
    "details": "Invalid address information provided"
  }
}"""

ParsedAddressValidationResponse = [
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "success": True,
            "complete_address": {
                "city": "City Name",
                "postal_code": "12345",
                "country_code": "US",
                "residential": False
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
            "code": "address_error",
            "message": "Unable to validate address",
            "details": {
                "details": "Invalid address information provided"
            }
        }
    ]
]