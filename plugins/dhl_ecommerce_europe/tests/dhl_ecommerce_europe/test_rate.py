import unittest
from unittest.mock import patch, ANY
from .fixture import gateway, RatePayload, RateRequest, RateResponse

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLEcommerceEuropeRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        # Check if the request structure is correct
        self.assertIn("plannedShippingDateAndTime", request.serialize())
        self.assertEqual(request.serialize()["productCode"], "V01PAK")

    def test_get_rate(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            # Check if the correct URL is being called
            self.assertIn("api", mock.call_args[1]["url"])

    def test_parse_rate_response(self):
        with patch("karrio.mappers.dhl_ecommerce_europe.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


ParsedRateResponse = [
    [
        {
            "carrier_id": "dhl_ecommerce_europe",
            "carrier_name": "dhl_ecommerce_europe",
            "currency": "EUR",
            "extra_charges": [
                {"amount": 20.0, "currency": "EUR", "name": "Base Price"},
                {"amount": 5.5, "currency": "EUR", "name": "Fuel Surcharge"},
            ],
            "meta": {
                "delivery_capabilities": {
                    "deliveryAdditionalDays": 0,
                    "deliveryDayOfWeek": 4,
                    "deliveryTypeCode": "QDDC",
                    "destinationFacilityAreaCode": "BER",
                    "destinationServiceAreaCode": "BER",
                    "estimatedDeliveryDateAndTime": "2025-01-22T17:00:00",
                    "totalTransitDays": 2,
                },
                "local_product_code": "V01PAK",
                "product_code": "V01PAK",
                "service_name": "DHL Parcel",
            },
            "service": "V01PAK",
            "total_charge": 25.5,
            "transit_days": 2,
        }
    ],
    [],
]
