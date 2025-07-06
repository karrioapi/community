"""Karrio ShipEngine client settings."""

import attr
import karrio.providers.shipengine.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """ShipEngine connection settings."""

    # Required: ShipEngine API Key
    api_key: str

    # Optional: Preferred carriers (if not specified, all available carriers used)
    carrier_ids: str = None  # Comma-separated carrier IDs
    
    # Optional: Account number (for compatibility with test fixtures)
    account_number: str = None

    # Standard Karrio fields (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "shipengine"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
