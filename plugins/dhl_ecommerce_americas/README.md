# karrio_dhl_ecommerce_americas

DHL eCommerce Americas shipping API integration for Karrio multi-carrier shipping SDK.

## Features

- **Rating** - Get shipping rates for DHL eCommerce Americas
- **Shipping** - Create and manage shipments
- **Tracking** - Track shipments in real-time
- **Address validation** - Validate shipping addresses

## Installation

```bash
pip install karrio_dhl_ecommerce_americas
```

## Settings

```python
import karrio

dhl_settings = karrio.Settings(
    carrier_id="dhl_ecommerce_americas",
    client_id="your_client_id",
    password="your_password",
    test_mode=True  # Use False for production
)
```

## Usage

```python
import karrio

# Create a rate request
rate_request = karrio.Rating.fetch({
    "shipper": {
        "postal_code": "10001",
        "country_code": "US"
    },
    "recipient": {
        "postal_code": "10002", 
        "country_code": "US"
    },
    "parcels": [{
        "weight": 1.5,
        "length": 10,
        "width": 8,
        "height": 6
    }]
}).from_(dhl_settings)

print(rate_request.parse())
```

## API Endpoints

- **Base URL**: `https://api.dhlecommerce.dhl.com`
- **Authentication**: OAuth (client_id + password)
- **Regions**: Americas (US, Canada, Latin America)

## Documentation

For detailed API documentation, visit: https://developer.dhl.com/api-reference/label-dhl-ecommerce-americas
