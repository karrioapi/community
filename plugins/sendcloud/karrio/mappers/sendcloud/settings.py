"""Karrio SendCloud client settings."""

import attr
import karrio.providers.sendcloud.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """SendCloud connection settings."""

    # Add carrier specific API connection properties here
    username: str
    password: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "sendcloud"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {} 
