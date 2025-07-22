"""Karrio DHL Express client settings."""

import attr
import karrio.providers.dhl_express.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DHL Express connection settings."""

    # required carrier specific properties
    username: str
    password: str
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_express"
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}
