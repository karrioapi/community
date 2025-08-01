"""Karrio MyDHL client settings."""

import attr
import karrio.providers.mydhl.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """MyDHL connection settings."""

    username: str
    password: str
    account_number: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "mydhl"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
