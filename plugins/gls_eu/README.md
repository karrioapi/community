# GLS EU Shipping Extension

This package is a GLS EU extension of the [karrio](https://pypi.org/project/karrio) multi-carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.gls_eu
```

## Usage

```python
import karrio
from karrio.mappers.gls_eu.settings import Settings

# Initialize carrier gateway
canadapost = karrio.gateway["gls_eu"].create(
    Settings(
        username="test_username",
        password="test_password",
        customer_id="2760",
        test_mode=True
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
