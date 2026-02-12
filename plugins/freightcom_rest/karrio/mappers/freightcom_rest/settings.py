"""Karrio Freightcom Rest client settings."""

import attr
import karrio.providers.freightcom_rest.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Freightcom Rest connection settings."""

    # Add carrier specific API connection properties here
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "freightcom_rest"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
