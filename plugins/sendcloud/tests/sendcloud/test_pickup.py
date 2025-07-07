"""SendCloud carrier pickup tests."""

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
        self.assertEqual(request.serialize(), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/PICKUP123"
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups/PICKUP123"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendcloud.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
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
    "ready_time": "09:00:00",
    "closing_time": "17:00:00"
}

PickupUpdatePayload = {
    "confirmation_number": "PICKUP123",
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
    "pickup_date": "2024-01-02",
    "ready_time": "10:00:00",
    "closing_time": "18:00:00"
}

PickupCancelPayload = {
    "confirmation_number": "PICKUP123",
    "reason": "Customer request"
}

PickupRequest = {
    "address": {
        "address_line1": "123 Test Street",
        "city": "Test City",
        "postal_code": "12345",
        "country_code": "US",
        "company_name": "Test Company",
        "contact_name": "Test Person",
        "phone_number": "1234567890",
        "email": "test@example.com"
    },
    "pickup_date": "2024-01-01",
    "ready_time": "09:00",
    "closing_time": "17:00"
}

PickupResponse = """{
  "id": "PICKUP123",
  "pickup_date": "2024-01-01",
  "ready_time": "09:00:00",
  "closing_time": "17:00:00",
  "status": "scheduled",
  "address": {
    "company_name": "Test Company",
    "address_line1": "123 Test Street",
    "city": "Test City",
    "postal_code": "12345",
    "country_code": "US"
  }
}"""

PickupUpdateResponse = """{
  "id": "PICKUP123",
  "pickup_date": "2024-01-02",
  "ready_time": "10:00",
  "closing_time": "18:00",
  "status": "updated"
}"""

PickupCancelResponse = """{
  "success": true,
  "message": "Pickup successfully cancelled",
  "id": "PICKUP123"
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
        "carrier_id": "sendcloud",
        "carrier_name": "sendcloud",
        "confirmation_number": "PICKUP123",
        "pickup_date": "2024-01-01",
        "pickup_charge": 0.0,
        "ready_time": "09:00",
        "closing_time": "17:00"
    },
    []
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "sendcloud",
            "carrier_name": "sendcloud",
            "code": "pickup_error",
            "details": {
                "details": "Invalid pickup date provided"
            },
            "message": "Unable to schedule pickup"
        }
    ]
]