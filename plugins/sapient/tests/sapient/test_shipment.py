import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import logging as logger

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSAPIENTShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment_request_small_item_weights(self):
        """Test that small item weights result in correct declared weight adjustment."""
        request = models.ShipmentRequest(**SmallWeightsShipmentPayload)
        serialized = gateway.mapper.create_shipment_request(request).serialize()

        self.assertEqual(serialized, SmallWeightsShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v4/shipments/RM",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v4/shipments/status",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.sapient.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "carrier_service",
    "shipper": {
        "company_name": "Company & Co.",
        "person_name": "Jane Smith",
        "address_line1": "10 Sky Lane",
        "address_line2": "Hashmoore House",
        "city": "Leatherhead",
        "postal_code": "AA34 3AB",
        "country_code": "GB",
        "person_name": "Jane Smith",
        "state_code": "Surrey",
        "phone_number": "607723456789",
        "email": "email@server.com",
    },
    "recipient": {
        "company_name": "Company & Co.",
        "person_name": "John Smith",
        "address_line1": "10 Sky Road",
        "address_line2": "10 Sky Road",
        "city": "Sydney",
        "postal_code": "2000",
        "country_code": "AU",
        "person_name": "John Smith",
        "state_code": "NSW",
        "phone_number": "07123456789",
        "email": "john.smith@example.com",
    },
    "return_address": {
        "company_name": "Company & Co.",
        "person_name": "John Smith",
        "address_line1": "Level 5",
        "address_line2": "Hashmoore House",
        "city": "Leatherhead",
        "postal_code": "AA34 3AB",
        "country_code": "GB",
        "person_name": "John Smith",
        "state_code": "Surrey",
        "phone_number": "07723456789",
        "email": "email@server.com",
    },
    "parcels": [
        {
            "weight": 1.5,
            "length": 40,
            "width": 30,
            "height": 20,
        }
    ],
    "options": {
        "shipment_date": "2024-08-11",
        "declared_value": 98.99,
        "sapient_customs_email": True,
        "sapient_customs_phone": True,
        "sapient_ebay_vtn": "ebay1234abc",
        "sapient_safeplace_location": "Under the doormat",
    },
    "customs": {
        "content_type": "merchandise",
        "incoterm": "DDU",
        "invoice": "INV-12345",
        "invoice_date": "2024-06-17",
        "options": {
            "eori_number": "GB213456789000",
            "vat_registration_number": "GB123456789",
        },
        "commodities": [
            {
                "title": "White Mens Large T-shirt",
                "quantity": 1,
                "weight": 0.5,
                "value_amount": 19.99,
                "origin_country": "CN",
                "hs_code": "6109100010",
                "sku": "SKU123",
            },
            {
                "title": "Black Mens Large Jumper",
                "quantity": 2,
                "weight": 0.3,
                "value_amount": 32.99,
                "origin_country": "CN",
                "hs_code": "6110113000",
                "sku": "SKU456",
            },
        ],
    },
    "reference": "OrderRef56",
}

ShipmentCancelPayload = {
    "shipment_identifier": "fa3bb603-2687-4b38-ba18-3264208446c6",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "docs": {
            "label": "jVBERw0KGgoAAAANSUhEUgAA.....A4QAAAXcCAYAAAB6Q0CbAAAAAXNSR0IArs4"
        },
        "label_type": "PDF",
        "meta": {
            "sapient_carrier_code": "RM",
            "rate_provider": "royalmail",
            "sapient_shipment_id": "fa3bb603-2687-4b38-ba18-3264208446c6",
            "shipment_ids": ["fa3bb603-2687-4b38-ba18-3264208446c6"],
            "tracking_numbers": ["TT123456785GB"],
        },
        "shipment_identifier": "fa3bb603-2687-4b38-ba18-3264208446c6",
        "tracking_number": "TT123456785GB",
    },
    [],
]

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "sapient",
        "carrier_name": "sapient",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "CarrierSpecifics": {
        "ServiceEnhancements": [
            {"Code": "CustomsEmail"},
            {"Code": "CustomsPhone"},
            {"Code": "Safeplace", "SafeplaceLocation": "Under the doormat"},
        ],
        "ServiceLevel": "02",
        "EbayVtn": "ebay1234abc",
    },
    "Customs": {
        "Incoterms": "DDU",
        "InvoiceDate": "2024-06-17",
        "InvoiceNumber": "INV-12345",
        "ReasonForExport": "Sale of Goods",
    },
    "Destination": {
        "Address": {
            "ContactName": "John Smith",
            "CompanyName": "Company & Co.",
            "ContactEmail": "john.smith@example.com",
            "ContactPhone": "07123456789",
            "CountryCode": "AU",
            "Line1": "10 Sky Road",
            "Line2": "10 Sky Road",
            "Postcode": "2000",
            "Town": "Sydney",
        }
    },
    "Items": [
        {
            "CountryOfOrigin": "CN",
            "Description": "White Mens Large T-shirt",
            "HSCode": "6109100010",
            "Quantity": 1,
            "SkuCode": "SKU123",
            "Value": 19.99,
            "Weight": 0.5,
        },
        {
            "CountryOfOrigin": "CN",
            "Description": "Black Mens Large Jumper",
            "HSCode": "6110113000",
            "Quantity": 2,
            "SkuCode": "SKU456",
            "Value": 32.99,
            "Weight": 0.3,
        },
    ],
    "Packages": [
        {
            "DeclaredWeight": 0.68,
            "Dimensions": {"Height": 50.8, "Length": 101.6, "Width": 76.2},
            "PackageType": "Parcel",
        }
    ],
    "ReturnToSender": {
        "Address": {
            "ContactName": "John Smith",
            "CompanyName": "Company & Co.",
            "ContactEmail": "email@server.com",
            "ContactPhone": "07723456789",
            "CountryCode": "GB",
            "Line1": "Level 5",
            "Line2": "Hashmoore House",
            "Postcode": "AA34 3AB",
            "Town": "Leatherhead",
        }
    },
    "ShipmentInformation": {
        "Action": "Process",
        "ContentType": "NDX",
        "CurrencyCode": "GBP",
        "DeclaredWeight": 0.68,
        "DescriptionOfGoods": "N/A",
        "DimensionsUnitOfMeasure": "CM",
        "LabelFormat": "PDF",
        "ServiceCode": "carrier_service",
        "ShipmentDate": ANY,
        "WeightUnitOfMeasure": "KG",
    },
    "Shipper": {
        "Address": {
            "ContactName": "Jane Smith",
            "CompanyName": "Company & Co.",
            "ContactEmail": "email@server.com",
            "ContactPhone": "607723456789",
            "CountryCode": "GB",
            "Line1": "10 Sky Lane",
            "Line2": "Hashmoore House",
            "Postcode": "AA34 3AB",
            "Town": "Leatherhead",
        },
        "Reference1": "OrderRef56",
        "EoriNumber": "GB213456789000",
        "VatNumber": "GB123456789",
        "ShippingAccountId": "shipping_account_id",
    },
}

ShipmentCancelRequest = {
    "ShipmentIds": ["fa3bb603-2687-4b38-ba18-3264208446c6"],
    "Status": "Cancel",
    "Reason": "Order Cancelled",
}


ShipmentResponse = """{
  "Labels": "jVBERw0KGgoAAAANSUhEUgAA.....A4QAAAXcCAYAAAB6Q0CbAAAAAXNSR0IArs4",
  "LabelFormat": "PDF",
  "Packages": [
    {
      "CarrierDetails": {
        "UniqueId": "3A07033860010000B2268"
      },
      "ShipmentId": "fa3bb603-2687-4b38-ba18-3264208446c6",
      "PackageOccurrence": 1,
      "TrackingNumber": "TT123456785GB",
      "CarrierTrackingUrl": "https://www.royalmail.com/track-your-item#/tracking-results/TT123456785GB"
    }
  ]
}
"""

ShipmentCancelResponse = """{"ok": true}"""


SmallWeightsShipmentPayload = {
    "service": "sapient_royal_mail_tracked_24",
    "shipper": {
        "company_name": "Test Warehouse Ltd",
        "person_name": "Warehouse Manager",
        "address_line1": "27 High Street",
        "city": "London",
        "postal_code": "WC1N 3AX",
        "country_code": "GB",
        "phone_number": "07849539027",
        "email": "warehouse@example.com",
    },
    "recipient": {
        "company_name": "Customer Corp",
        "person_name": "Test Customer",
        "address_line1": "Unit 3, Business Park",
        "address_line2": "Industrial Road",
        "city": "Manchester",
        "postal_code": "M1 2AB",
        "country_code": "GB",
        "phone_number": "07557544686",
        "email": "customer@example.com",
    },
    "parcels": [
        {
            "weight": 0.12,
            "weight_unit": "KG",
            "length": 27,
            "width": 20,
            "height": 3,
            "dimension_unit": "CM",
            "items": [
                {
                    "title": "Electronic Component A",
                    "description": "Small electronic component",
                    "origin_country": "PH",
                    "quantity": 4,
                    "sku": "COMP-A",
                    "value_amount": 2.95,
                    "value_currency": "GBP",
                    "weight": 0.005,
                    "weight_unit": "KG",
                },
                {
                    "title": "Electronic Component B",
                    "description": "Small electronic component",
                    "origin_country": "MY",
                    "quantity": 4,
                    "sku": "COMP-B",
                    "value_amount": 2.95,
                    "value_currency": "GBP",
                    "weight": 0.005,
                    "weight_unit": "KG",
                },
                {
                    "title": "Electronic Component C",
                    "description": "Tiny electronic component",
                    "origin_country": "JP",
                    "quantity": 4,
                    "sku": "COMP-C",
                    "value_amount": 0.95,
                    "value_currency": "GBP",
                    "weight": 0.001,
                    "weight_unit": "KG",
                },
                {
                    "title": "Electronic Component D",
                    "description": "Small electronic component",
                    "origin_country": "CN",
                    "quantity": 3,
                    "sku": "COMP-D",
                    "value_amount": 0.95,
                    "value_currency": "GBP",
                    "weight": 0.002,
                    "weight_unit": "KG",
                },
                {
                    "title": "Electronic Component E",
                    "description": "Small electronic component",
                    "origin_country": "CN",
                    "quantity": 3,
                    "sku": "COMP-E",
                    "value_amount": 0.95,
                    "value_currency": "GBP",
                    "weight": 0.005,
                    "weight_unit": "KG",
                },
                {
                    "title": "Electronic Component F",
                    "description": "Small electronic component",
                    "origin_country": "CN",
                    "quantity": 4,
                    "sku": "COMP-F",
                    "value_amount": 0.95,
                    "value_currency": "GBP",
                    "weight": 0.002,
                    "weight_unit": "KG",
                },
            ],
        }
    ],
    "options": {
        "shipment_date": "2024-08-11",
        "declared_value": 36.9,
        "currency": "GBP",
    },
    "reference": "ORDER-12345",
}

SmallWeightsShipmentRequest = {
    "CarrierSpecifics": {
        "ServiceLevel": "02",
    },
    "Destination": {
        "Address": {
            "CompanyName": "Customer Corp",
            "ContactEmail": "customer@example.com",
            "ContactName": "Test Customer",
            "ContactPhone": "07557544686",
            "CountryCode": "GB",
            "Line1": "Unit 3, Business Park",
            "Line2": "Industrial Road",
            "Postcode": "M1 2AB",
            "Town": "Manchester",
        }
    },
    "Items": [
        {
            "CountryOfOrigin": "PH",
            "Description": "Electronic Component A",
            "Quantity": 4,
            "SkuCode": "COMP-A",
            "Value": 2.95,
            "Weight": 0.01,
        },
        {
            "CountryOfOrigin": "MY",
            "Description": "Electronic Component B",
            "Quantity": 4,
            "SkuCode": "COMP-B",
            "Value": 2.95,
            "Weight": 0.01,
        },
        {
            "CountryOfOrigin": "JP",
            "Description": "Electronic Component C",
            "Quantity": 4,
            "SkuCode": "COMP-C",
            "Value": 0.95,
            "Weight": 0.001,
        },
        {
            "CountryOfOrigin": "CN",
            "Description": "Electronic Component D",
            "Quantity": 3,
            "SkuCode": "COMP-D",
            "Value": 0.95,
            "Weight": 0.002,
        },
        {
            "CountryOfOrigin": "CN",
            "Description": "Electronic Component E",
            "Quantity": 3,
            "SkuCode": "COMP-E",
            "Value": 0.95,
            "Weight": 0.01,
        },
        {
            "CountryOfOrigin": "CN",
            "Description": "Electronic Component F",
            "Quantity": 4,
            "SkuCode": "COMP-F",
            "Value": 0.95,
            "Weight": 0.002,
        },
    ],
    "Packages": [
        {
            # DeclaredWeight adjusted to 0.13 (>= items total 0.128, rounded to 2 decimals)
            # Original: 0.12, but items total after rounding: 0.128
            "DeclaredValue": 36.9,
            "DeclaredWeight": 0.13,
            "Dimensions": {"Height": 3.0, "Length": 27.0, "Width": 20.0},
            "PackageType": "Parcel",
        }
    ],
    "ShipmentInformation": {
        "Action": "Process",
        "ContentType": "NDX",
        "CurrencyCode": "GBP",
        # DeclaredWeight adjusted to 0.13 (>= items total 0.128, rounded to 2 decimals)
        "DeclaredWeight": 0.13,
        "DescriptionOfGoods": "Electronic Component A Electronic Component B Electronic Component C E",
        "DimensionsUnitOfMeasure": "CM",
        "LabelFormat": "PDF",
        "ServiceCode": "sapient_royal_mail_tracked_24",
        "ShipmentDate": ANY,
        "WeightUnitOfMeasure": "KG",
    },
    "Shipper": {
        "Address": {
            "CompanyName": "Test Warehouse Ltd",
            "ContactEmail": "warehouse@example.com",
            "ContactName": "Warehouse Manager",
            "ContactPhone": "07849539027",
            "CountryCode": "GB",
            "Line1": "27 High Street",
            "Postcode": "WC1N 3AX",
            "Town": "London",
        },
        "Reference1": "ORDER-12345",
        "ShippingAccountId": "shipping_account_id",
    },
}
