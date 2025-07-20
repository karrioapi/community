
# karrio.dhl_ecommerce_europe

This package is a DHL eCommerce Europe extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_ecommerce_europe
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dhl_ecommerce_europe.settings import Settings


# Initialize a carrier gateway
dhl_ecommerce_europe = karrio.gateway["dhl_ecommerce_europe"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
