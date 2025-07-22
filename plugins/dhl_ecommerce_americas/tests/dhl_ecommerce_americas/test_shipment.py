import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, ShipmentPayload, ShipmentResponse, ShipmentCancelPayload, ShipmentCancelRequest, ShipmentCancelResponse

import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceAmericasShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        
        # Verify basic structure
        serialized = request.serialize()
        self.assertIn("header", serialized)
        self.assertIn("body", serialized)
        self.assertEqual(serialized["header"]["messageType"], "LABEL")
        self.assertEqual(serialized["body"]["productCode"], "DHLParcelGround")

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = "{}"
            
            # Test request creation and proxy call
            request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
            response = gateway.proxy.create_shipment(request)

            # Check OAuth call
            oauth_call = mock.call_args_list[0]
            self.assertIn("OAuth/AccessToken", oauth_call[1]["url"])
            
            # Check shipment call
            shipment_call = mock.call_args_list[1]
            self.assertEqual(
                shipment_call[1]["url"],
                f"{gateway.settings.server_url}/rest/v2/label",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = "{}"
            
            # Test request creation and proxy call
            request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
            response = gateway.proxy.cancel_shipment(request)

            # Check OAuth call
            oauth_call = mock.call_args_list[0]
            self.assertIn("OAuth/AccessToken", oauth_call[1]["url"])
            
            # Check cancel call
            cancel_call = mock.call_args_list[1]
            self.assertEqual(
                cancel_call[1]["url"],
                f"{gateway.settings.server_url}/rest/v2/shipment/PKG_1/cancel",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            
            request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
            response = gateway.proxy.create_shipment(request)
            parsed_response = gateway.mapper.parse_shipment_response(response)

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.dhl_ecommerce_americas.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            
            request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
            response = gateway.proxy.cancel_shipment(request)
            parsed_response = gateway.mapper.parse_cancel_shipment_response(response)

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ParsedShipmentResponse = [
    {
        "carrier_id": "dhl_ecommerce_americas",
        "carrier_name": "dhl_ecommerce_americas",
        "docs": {
            "label": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        },
        "meta": {
            "label_format": "PNG",
            "label_size": "4x6",
            "ordered_product_id": "ORDER_123456",
            "package_id": "PKG_1",
            "service_name": "DHL eCommerce Americas",
        },
        "shipment_identifier": "PKG_1",
        "tracking_number": "9374869903500938123456",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "dhl_ecommerce_americas",
        "carrier_name": "dhl_ecommerce_americas",
        "operation": "cancel shipment",
        "success": True,
    },
    [],
]
