"""Karrio Easyship client settings."""

import attr
import karrio.providers.easyship.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Easyship connection settings."""

    access_token: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "easyship"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
