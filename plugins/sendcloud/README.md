# Karrio Sendcloud Extension

Karrio extension for the Sendcloud shipping service.

## Documentation

Please visit [sendcloud.dev](https://api.sendcloud.dev/docs/sendcloud-public-api) for the latest API documentation.

## Installation

```bash
pip install karrio_sendcloud
```

## Usage

```python
import karrio
from karrio.mappers.sendcloud import Settings

# Initialize the settings
settings = Settings(
    public_key="your_public_key",
    secret_key="your_secret_key",
    test_mode=True
)

# Create a carrier gateway
gateway = karrio.gateway["sendcloud"].create(settings)
```

## Authentication

Sendcloud uses API key authentication. You'll need to obtain your public and secret keys from your Sendcloud dashboard.

## Features

- Rate calculation
- Shipment creation
- Tracking
- Address validation
