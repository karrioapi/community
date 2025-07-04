# karrio.veho

This package is a Veho extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.veho
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.veho.settings import Settings


# Initialize a carrier gateway
veho = karrio.gateway["veho"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
