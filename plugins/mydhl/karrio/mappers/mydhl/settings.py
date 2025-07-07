"""Karrio MyDHL client settings."""

import attr
import jstruct
import karrio.lib as lib
import karrio.providers.mydhl.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """MyDHL connection settings."""

    # MyDHL API credentials (required)
    username: str                   # MyDHL API username
    password: str                   # MyDHL API password
    account_number: str             # MyDHL customer account number

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "mydhl"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
