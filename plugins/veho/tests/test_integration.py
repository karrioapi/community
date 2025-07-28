import unittest
from karrio.core.models import RateRequest, Address
from karrio.mappers.veho.settings import Settings
from karrio.providers.veho.rate import rate_request, parse_rate_response
import karrio.lib as lib


class TestVehoIntegration(unittest.TestCase):

    def setUp(self):
        self.settings = Settings(
            api_key="test_api_key",
            test_mode=True
        )
    
    def test_rate_request_creation(self):
        """Test that rate requests are created properly."""
        payload = RateRequest(
            shipper=Address(
                postal_code="10001",
                city="New York",
                country_code="US"
            ),
            recipient=Address(
                postal_code="90210",
                city="Beverly Hills",
                country_code="US"
            ),
            parcels=[{
                "weight": 5.0,
                "length": 10.0,
                "width": 8.0,
                "height": 6.0
            }]
        )
        
        request = rate_request(payload, self.settings)
        data = request.serialize()
        
        self.assertEqual(data["originationZip"], "10001")
        self.assertEqual(data["deliveryZip"], "90210")
        self.assertEqual(len(data["packages"]), 1)
        self.assertEqual(data["serviceClass"], "groundPlus")


if __name__ == "__main__":
    unittest.main() 
