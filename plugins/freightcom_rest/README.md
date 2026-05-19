# karrio.freightcom_rest

This package is a Freightcom Rest extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.freightcom_rest
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.freightcom_rest.settings import Settings


# Initialize a carrier gateway
freightcom_rest = karrio.gateway["freightcom_rest"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
