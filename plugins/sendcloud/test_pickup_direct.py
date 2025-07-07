#!/usr/bin/env python
"""Test pickup functionality directly"""

import unittest
from unittest.mock import patch
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

# Test data
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
    "closing_time": "17:00"
}

PickupCancelPayload = {
    "confirmation_number": "PICKUP123",
    "reason": "Customer request"
}

class TestPickupDirect(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_pickup_request_creation(self):
        """Test that pickup request creation works"""
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        result = request.serialize()
        print(f"✓ Pickup request created: {result}")
        
        # Basic validation
        self.assertIsInstance(result, dict)
        self.assertIn("pickup_date", result)
        self.assertIn("ready_time", result)
        self.assertIn("closing_time", result)

    def test_pickup_cancel_request_creation(self):
        """Test that pickup cancel request creation works"""
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
        result = request.serialize()
        print(f"✓ Pickup cancel request created: {result}")
        
        # Basic validation
        self.assertIsInstance(result, str)  # Cancel requests usually just return the confirmation number
        self.assertEqual(result, "PICKUP123")

if __name__ == "__main__":
    print("🧪 Testing SendCloud Pickup Functionality")
    print("=" * 50)
    unittest.main(verbosity=2)