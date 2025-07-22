import unittest
from unittest.mock import patch, Mock
import karrio.core.models as models
import karrio.sdk as karrio
from karrio.mappers.dhl_express.settings import Settings
from tests.dhl_express.fixture import gateway, ShipmentPayload, ShipmentResponse


class TestDHLExpressShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    @patch("karrio.mappers.dhl_express.proxy.lib.request")
    def test_create_shipment(self, mock_request):
        mock_request.return_value = ShipmentResponse
        shipment, messages = karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
        
        self.assertEqual(
            mock_request.call_args[1]["url"],
            f"{gateway.settings.server_url}/shipments",
        )
        self.assertEqual(shipment.tracking_number, "1234567890")
        self.assertIsNotNone(shipment.docs)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        
        # Check if the request structure is correct
        request_data = request.serialize()
        self.assertIn("plannedShippingDateAndTime", request_data)
        self.assertIn("customerDetails", request_data)
        self.assertIn("packages", request_data)
        self.assertIn("content", request_data)

    def test_parse_shipment_response(self):
        parsed_response = gateway.mapper.parse_shipment_response(
            Mock(deserialize=lambda: ShipmentResponse)
        )
        shipment, messages = parsed_response
        
        self.assertEqual(shipment.tracking_number, "1234567890")
        self.assertIsNotNone(shipment.docs)

    @patch("karrio.mappers.dhl_express.proxy.lib.request")
    def test_cancel_shipment(self, mock_request):
        mock_request.return_value = {"cancelled": True}
        cancel_request = models.ShipmentCancelRequest(shipment_identifier="1234567890")
        confirmation, messages = karrio.Shipment.cancel(cancel_request).from_(gateway).parse()
        
        self.assertTrue(confirmation.success)
        self.assertEqual(confirmation.operation, "Cancel Shipment")


if __name__ == "__main__":
    unittest.main()
