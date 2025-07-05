"""Karrio SendCloud client settings."""

import attr
import karrio.providers.sendcloud.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """SendCloud connection settings."""

    # API credentials for SendCloud API v2/v3
    client_id: str
    client_secret: str

    # Optional settings
    sender_address_id: int = None
    test_mode: bool = False
    
    # generic properties
    id: str = None
    carrier_id: str = "sendcloud"
    account_country_code: str = "NL"
    metadata: dict = {}
    config: dict = {}
