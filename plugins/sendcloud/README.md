# karrio.sendcloud

This package is a SendCloud extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.sendcloud
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.sendcloud.settings import Settings


# Initialize a carrier gateway
sendcloud = karrio.gateway["sendcloud"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
