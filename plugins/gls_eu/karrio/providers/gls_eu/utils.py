import base64
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """GLS EU connection settings."""

    username: str
    password: str
    customer_id: str = None

    @property
    def carrier_name(self):
        return "gls_eu"

    @property
    def server_url(self):
        return (
            "https://sandbox.api.gls-eu.com/v1" if self.test_mode else "https://api.gls-eu.com/v1"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.gls_eu.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def authorization(self):
        pair = f"{self.username}:{self.password}"
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")


class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str)
