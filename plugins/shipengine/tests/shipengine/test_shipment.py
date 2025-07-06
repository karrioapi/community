"""ShipEngine carrier shipment tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

logger = logging.getLogger(__name__)

class TestShipEngineShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_shipment_cancel_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/labels/SHIP123456/void"
            )

    def test_parse_shipment_cancel_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.shipengine.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
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
    ],
    "service": "shipengine_ups_ups_ground"
}

ShipmentCancelPayload = {
    "shipment_identifier": "SHIP123456"
}

ShipmentRequest = {
    "label_format": "pdf",
    "label_layout": "4x6",
    "shipment": {
        "service_code": "ups_ground",
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
                }
            }
        ]
    }
}

ShipmentCancelRequest = {
    "label_id": "SHIP123456"
}

ShipmentResponse = """{
  "label_id": "se-label-123456",
  "shipment_id": "se-shipment-789012",
  "tracking_number": "1Z999AA1234567890",
  "carrier_id": "se-carrier-345678",
  "carrier_code": "ups",
  "service_code": "ups_ground",
  "label_download": {
    "pdf": "https://api.shipengine.com/v1/downloads/labels/se-label-123456.pdf"
  }
}"""

ShipmentCancelResponse = """{
  "success": true,
  "message": "Shipment successfully cancelled"
}"""

ErrorResponse = """{
  "errors": [
    {
      "error_code": "shipment_error",
      "message": "Unable to create shipment",
      "error_source": "shipengine",
      "error_type": "validation",
      "field_name": "shipment",
      "field_value": "Invalid shipment information provided"
    }
  ]
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "shipengine",
        "carrier_name": "shipengine",
        "tracking_number": "1Z999AA1234567890",
        "shipment_identifier": "se-label-123456",
        "docs": {
            "label": "https://api.shipengine.com/v1/downloads/labels/se-label-123456.pdf"
        },
        "meta": {
            "carrier_code": "ups",
            "service_code": "ups_ground",
            "label_format": "PDF",
            "shipment_id": "se-shipment-789012",
            "carrier_id": "se-carrier-345678",
            "tracking_url": "https://www.shipengine.com/tracking/1Z999AA1234567890"
        }
    },
    []
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "shipengine",
        "carrier_name": "shipengine",
        "success": True,
        "operation": "cancel"
    },
    []
]

ParsedErrorResponse = [
    {
        "carrier_id": "shipengine",
        "carrier_name": "shipengine",
        "docs": {},
        "meta": {
            "label_format": "PDF",
            "tracking_url": "https://www.shipengine.com/tracking/"
        }
    },
    [
        {
            "carrier_id": "shipengine",
            "carrier_name": "shipengine",
            "code": "shipment_error",
            "message": "Unable to create shipment",
            "details": {
                "error_source": "shipengine",
                "error_type": "validation",
                "field_name": "shipment",
                "field_value": "Invalid shipment information provided"
            }
        }
    ]
]