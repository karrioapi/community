import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Easyship connection settings."""

    access_token: str

    @property
    def carrier_name(self):
        return "easyship"

    @property
    def server_url(self):
        return "https://api.easyship.com"

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""

    platform_name = lib.OptionEnum("platform_name")
    apply_shipping_rules = lib.OptionEnum("apply_shipping_rules", bool)
    allow_courier_fallback = lib.OptionEnum("allow_courier_fallback", bool)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
