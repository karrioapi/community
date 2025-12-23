"""Locate2u connection settings."""

import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Locate2u connection settings."""

    client_id: str = None
    client_secret: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "locate2u"
    account_country_code: str = "AU"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "locate2u"

    @property
    def server_url(self):
        return "https://api.locate2u.com"

    @property
    def auth_server_url(self):
        return "https://id.locate2u.com"
