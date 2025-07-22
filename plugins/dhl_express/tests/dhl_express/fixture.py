import karrio.sdk as karrio
import karrio.core.models as models

gateway = karrio.gateway["dhl_express"].create(
    dict(
        username="test_username",
        password="test_password", 
        account_number="123456789",
        test_mode=True,
    )
)

# Test payload for rate requests
RatePayload = {
    "shipper": {
        "company_name": "Test Company",
        "person_name": "John Doe",
        "phone_number": "+1234567890",
        "email": "shipper@test.com",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
    },
    "recipient": {
        "company_name": "Recipient Company", 
        "person_name": "Jane Smith",
        "phone_number": "+447123456789",
        "email": "recipient@test.com",
        "address_line1": "10 Downing St",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
    },
    "parcels": [
        {
            "weight": 1.5,
            "length": 10,
            "width": 10,
            "height": 5,
        }
    ],
    "services": ["EXPRESS_WORLDWIDE"],
    "options": {
        "pickup_date": "2023-07-01",
    },
}

# Test payload for shipment requests
ShipmentPayload = {
    "shipper": {
        "company_name": "Test Company",
        "person_name": "John Doe",
        "phone_number": "+1234567890",
        "email": "shipper@test.com",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
    },
    "recipient": {
        "company_name": "Recipient Company", 
        "person_name": "Jane Smith",
        "phone_number": "+447123456789",
        "email": "recipient@test.com",
        "address_line1": "10 Downing St",
        "city": "London",
        "postal_code": "SW1A 1AA",
        "country_code": "GB",
    },
    "parcels": [
        {
            "weight": 1.5,
            "length": 10,
            "width": 10,
            "height": 5,
        }
    ],
    "service": "EXPRESS_WORLDWIDE",
    "options": {
        "pickup_date": "2023-07-01",
    },
    "reference": "REF123",
}

# Mock rate response
RateResponse = {
    "products": [
        {
            "productName": "DHL Express Worldwide",
            "productCode": "EXPRESS_WORLDWIDE",
            "totalPrice": [
                {
                    "currencyType": "USD",
                    "price": "45.50"
                }
            ],
            "deliveryCapabilities": {
                "totalTransitDays": "1"
            },
        }
    ]
}

# Mock shipment response
ShipmentResponse = {
    "shipmentTrackingNumber": "1234567890",
    "documents": [
        {
            "imageFormat": "PDF",
            "content": "JVBERi0xLjQKJeLjz9MKM...",
            "typeCode": "label"
        }
    ]
}

# Mock tracking response
TrackingResponse = {
    "shipments": [
        {
            "shipmentTrackingNumber": "1234567890",
            "status": {
                "statusCode": "transit",
                "description": "Shipment is in transit"
            },
            "events": [
                {
                    "timestamp": "2023-07-01T10:00:00",
                    "typeCode": "PU",
                    "description": "Shipment picked up",
                    "location": {
                        "address": {
                            "addressLocality": "New York",
                            "postalCode": "10001",
                            "countryCode": "US"
                        }
                    }
                }
            ]
        }
    ]
}
