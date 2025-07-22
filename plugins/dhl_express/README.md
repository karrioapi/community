# karrio.dhl_express

This package is a DHL Express MyDHL API extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_express
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.dhl_express.settings import Settings


# Initialize a carrier gateway
dhl_express = karrio.gateway["dhl_express"].create(
    Settings(
        username="your_username",
        password="your_password",
        account_number="your_account_number",
        test_mode=True
    )
)
```

Check the [Karrio Multi-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
