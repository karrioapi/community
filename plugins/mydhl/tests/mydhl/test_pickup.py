"""MyDHL carrier pickup tests."""

import unittest
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models
from unittest.mock import patch
from .fixture import gateway


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")  # MANDATORY DEBUG PRINT
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")  # MANDATORY DEBUG PRINT
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mydhlapi/pickups"
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")  # MANDATORY DEBUG PRINT
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mydhlapi/pickups/123"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")  # MANDATORY DEBUG PRINT
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/mydhlapi/pickups/123"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")  # MANDATORY DEBUG PRINT
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "address": {
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
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00",
}

PickupUpdatePayload = {
    "confirmation_number": "123",
    "address": {
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
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00"
}

PickupCancelPayload = {
    "confirmation_number": "123",
    "pickup_date": "2024-01-01",
    "reason": "Schedule change"
}

PickupRequest = {
    "accounts": [
        {
            "number": "123456789",
            "typeCode": "shipper"
        }
    ],
    "closeTime": "17:00",
    "customerDetails": {
        "shipperDetails": {
            "contactInformation": {
                "companyName": "Test Company",
                "email": "test@example.com",
                "fullName": "Test Person",
                "phone": "1234567890"
            },
            "postalAddress": {
                "addressLine1": "123 Test Street",
                "cityName": "Test City",
                "countryCode": "US",
                "postalCode": "12345"
            }
        }
    },
    "location": "reception",
    "plannedPickupDateAndTime": "2024-01-01T00:00:00 GMT+01:00",
    "shipmentDetails": [
        {
            "packages": [
                {
                    "dimensions": {
                        "height": 1,
                        "length": 1,
                        "width": 1
                    },
                    "weight": 1.0
                }
            ],
            "productCode": "U"
        }
    ]
}

PickupResponse = """{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-01",
  "readyTime": "09:00",
  "closingTime": "17:00",
  "status": "scheduled"
}"""

PickupUpdateResponse = """{
  "confirmationNumber": "PICKUP123",
  "pickupDate": "2024-01-02",
  "readyTime": "10:00",
  "closingTime": "18:00",
  "status": "updated"
}"""

PickupCancelResponse = """{
  "success": true,
  "message": "Pickup successfully cancelled"
}"""

ErrorResponse = """{
  "error": {
    "code": "pickup_error",
    "message": "Unable to schedule pickup",
    "details": "Invalid pickup date provided"
  }
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "mydhl",
        "carrier_name": "mydhl",
        "confirmation_number": "PICKUP123",
        "pickup_date": "2024-01-01",
        "ready_time": "09:00",
        "closing_time": "17:00",
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "mydhl",
            "carrier_name": "mydhl",
            "code": "pickup_error",
            "message": "Unable to schedule pickup",
            "details": {
                "details": "Invalid pickup date provided"
            }
        }
    ]
]