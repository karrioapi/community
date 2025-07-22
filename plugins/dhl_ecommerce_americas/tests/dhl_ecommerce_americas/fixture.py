import karrio.lib as lib
import karrio.core.models as models
import karrio.mappers.dhl_ecommerce_americas.settings as provider_settings
from karrio.mappers.dhl_ecommerce_americas.proxy import Proxy
from karrio.mappers.dhl_ecommerce_americas.mapper import Mapper

# Create gateway manually since plugin might not be registered yet
settings = provider_settings.Settings(
    client_id="test_client_id",
    password="test_password", 
    test_mode=True,
)

class TestGateway:
    def __init__(self, settings):
        self.settings = settings
        self.mapper = Mapper(settings)
        self.proxy = Proxy(settings)

gateway = TestGateway(settings)

# Test payload for rate requests
RatePayload = {
    "shipper": {
        "company_name": "Test Company",
        "person_name": "John Doe",
        "phone_number": "+14155551234",
        "email": "shipper@test.com",
        "address_line1": "123 Main Street",
        "city": "New York",
        "postal_code": "10001",
        "state_code": "NY",
        "country_code": "US",
    },
    "recipient": {
        "company_name": "Recipient Company", 
        "person_name": "Jane Smith",
        "phone_number": "+13105551234",
        "email": "recipient@test.com",
        "address_line1": "456 Oak Avenue",
        "city": "Los Angeles",
        "postal_code": "90210",
        "state_code": "CA",
        "country_code": "US",
    },
    "parcels": [
        {
            "weight": 1.5,
            "length": 10,
            "width": 8, 
            "height": 6,
            "weight_unit": "LB",
            "dimension_unit": "IN",
        }
    ],
    "services": ["DHLParcelGround"],
}

# Test payload for shipment requests
ShipmentPayload = {
    "service": "DHLParcelGround",
    "shipper": RatePayload["shipper"],
    "recipient": RatePayload["recipient"],
    "parcels": RatePayload["parcels"],
}

# Test payload for tracking requests
TrackingPayload = {
    "tracking_numbers": ["9374869903500938123456"],
}

# Expected rate request - exactly matching actual output
RateRequest = {
    "consigneeAddress": {
        "city": "Los Angeles",
        "countryCode": "US",
        "postalCode": "90210",
        "state": "CA"
    },
    "consignorAddress": {
        "city": "New York",
        "countryCode": "US",
        "postalCode": "10001",
        "state": "NY"
    },
    "packages": [
        {
            "dimensions": {
                "dimensionUom": "IN",
                "height": 6.0,
                "length": 10.0,
                "width": 8.0
            },
            "weight": 1.5,
            "weightUom": "LB"
        }
    ],
    "productCode": "DHLParcelGround"
}

# Expected rate response
RateResponse = """{
  "header": {
    "code": 200,
    "message": "Success",
    "messageDetail": "Operation completed successfully"
  },
  "body": {
    "rates": [
      {
        "productCode": "DHLParcelGround",
        "productName": "DHL Parcel Ground",
        "totalCharge": 12.50,
        "currency": "USD",
        "transitTime": 3,
        "deliveryGuarantee": false,
        "charges": [
          {
            "chargeType": "Base Rate",
            "chargeAmount": 10.00
          },
          {
            "chargeType": "Fuel Surcharge",
            "chargeAmount": 2.50
          }
        ]
      }
    ]
  }
}"""

# Expected shipment response
ShipmentResponse = """{
  "header": {
    "code": 200,
    "message": "Success",
    "messageDetail": "Label created successfully"
  },
  "body": {
    "packageResults": [
      {
        "packageId": "PKG_1",
        "trackingNumber": "9374869903500938123456",
        "orderedProductId": "ORDER_123456",
        "labelImage": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
        "labelFormat": "PNG",
        "labelSize": "4x6"
      }
    ]
  }
}"""

# Expected tracking response 
TrackingResponse = """{
  "header": {
    "code": 200,
    "message": "Success",
    "messageDetail": "Tracking information retrieved"
  },
  "body": {
    "trackingNumber": "9374869903500938123456",
    "status": "in_transit",
    "events": [
      {
        "eventDate": "2025-01-20",
        "eventTime": "10:30:00",
        "eventDescription": "Package picked up",
        "location": "New York, NY",
        "eventCode": "PU"
      },
      {
        "eventDate": "2025-01-22", 
        "eventTime": "14:45:00",
        "eventDescription": "Out for delivery",
        "location": "Los Angeles, CA",
        "eventCode": "OFD"
      }
    ],
    "deliveryDate": "2025-01-23",
    "deliveryTime": "16:30:00",
    "signedBy": null
  }
}"""

# Shipment cancel request and response
ShipmentCancelPayload = {
    "shipment_identifier": "PKG_1",
}

ShipmentCancelRequest = {
    "shipment_id": "PKG_1"
}

ShipmentCancelResponse = """{
  "header": {
    "code": 200,
    "message": "Success",
    "messageDetail": "Shipment cancelled successfully"
  },
  "body": {
    "packageId": "PKG_1",
    "status": "cancelled"
  }
}"""
