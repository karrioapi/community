"""ShipEngine carrier address validation tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)


class TestShipEngineAddress(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = models.AddressValidationRequest(**AddressValidationPayload)

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(self.AddressValidationRequest)
        self.assertEqual(lib.to_dict(request.serialize()), AddressValidationRequest)

    def test_validate_address(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/addresses/validate"
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedAddressValidationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )
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
    "street_address": "123 Main St",
    "city_locality": "City Name",
    "postal_code": 12345,
    "country_code": "US",
    "state_province": "CA"
}

AddressValidationResponse = """{
  "is_valid": true,
  "normalized_address": {
    "street_address": "123 MAIN ST",
    "city_locality": "CITY NAME",
    "postal_code": "12345",
    "country_code": "US",
    "state_province": "CA"
  },
  "validation_messages": [
    {
      "message": "Address is valid",
      "code": "SUCCESS"
    }
  ]
}"""

ErrorResponse = """{
  "errors": [
    {
      "error_code": "address_error",
      "message": "Unable to validate address",
      "error_source": "shipengine",
      "error_type": "validation",
      "field_name": "address",
      "field_value": "Invalid address information provided"
    }
  ]
}"""

ParsedAddressValidationResponse = [
    {
        "carrier_id": "shipengine",
        "carrier_name": "shipengine",
        "complete_address": {
            "address_line1": "123 MAIN ST",
            "city": "CITY NAME",
            "country_code": "US",
            "postal_code": "12345",
            "residential": False,
            "state_code": "CA"
        },
        "success": True
    },
    []
]

ParsedErrorResponse = [
    {
        "carrier_id": "shipengine",
        "carrier_name": "shipengine",
        "success": False
    },
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "code": "address_error",
            "message": "Unable to validate address",
            "details": {
                "error_source": "shipengine",
                "error_type": "validation",
                "field_name": "address",
                "field_value": "Invalid address information provided"
            }
        }
    ]
]