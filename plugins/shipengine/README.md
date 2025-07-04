# karrio.shipengine

This package is a ShipEngine extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.shipengine
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.shipengine.settings import Settings


# Initialize a carrier gateway
shipengine = karrio.gateway["shipengine"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
