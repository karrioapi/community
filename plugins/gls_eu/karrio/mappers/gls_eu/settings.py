import attr
import karrio.providers.gls_eu.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """GLS EU connection settings."""

    username: str
    password: str
    customer_id: str = None

    # generic properties (do not modify)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "gls_eu"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
