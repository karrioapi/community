# karrio.sendcloud

This package is a SendCloud extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.sendcloud
```

## Usage

```python
import karrio
from karrio.mappers.sendcloud.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["sendcloud"].create(
    Settings(
        username="your_sendcloud_username",
        password="your_sendcloud_password",
        test_mode=True
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
