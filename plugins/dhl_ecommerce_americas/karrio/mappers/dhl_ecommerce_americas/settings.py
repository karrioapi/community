"""Karrio DHL eCommerce Americas settings."""

import attr
import karrio.providers.dhl_ecommerce_americas.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DHL eCommerce Americas connection settings."""
    
    client_id: str
    password: str
    test_mode: bool = False
    id: str = None
    carrier_id: str = "dhl_ecommerce_americas"
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}
