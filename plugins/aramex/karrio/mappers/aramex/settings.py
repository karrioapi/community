"""Karrio Aramex settings."""

import attr
from karrio.providers.aramex.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Aramex connection settings."""

    username: str
    password: str
    account_pin: str
    account_entity: str
    account_number: str
    account_country_code: str

    id: str = None
    test_mode: bool = False
    carrier_id: str = "aramex"
    metadata: dict = {}
    config: dict = {}
