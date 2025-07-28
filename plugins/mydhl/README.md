# karrio.mydhl

This package is a MyDHL Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.mydhl
```

## Usage

```python
import karrio
from karrio.mappers.mydhl.settings import Settings


# Initialize a carrier gateway
mydhl = karrio.gateway["mydhl"].create(
    Settings(
        site_id="your_site_id",
        password="your_password",
        account_number="your_account_number",
        test=True,
    )
)
```

Check the [Karrio Multi-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

## API Reference

- [MyDHL Express API Documentation](https://developer.dhl.com/api-reference/dhl-express-mydhl-api)
