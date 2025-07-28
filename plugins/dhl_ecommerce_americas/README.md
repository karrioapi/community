# karrio.dhl_ecommerce_americas

This package is a DHL eCommerce Americas extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_ecommerce_americas
```

## Usage

```python
import karrio
from karrio.mappers.dhl_ecommerce_americas.settings import Settings


# Initialize a carrier gateway
dhl = karrio.gateway["dhl_ecommerce_americas"].create(
    Settings(
        username="your_username",
        password="your_password",
        account_number="your_account_number",
        test=True,
    )
)
```

Check the [Karrio Multi-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

## API Reference

- [DHL eCommerce Americas API Documentation](https://developer.dhl.com/api-reference/label-dhl-ecommerce-americas)
