"""Karrio Sendcloud client settings."""

import attr
import karrio.providers.sendcloud.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Sendcloud connection settings."""

    public_key: str
    secret_key: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "sendcloud"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
