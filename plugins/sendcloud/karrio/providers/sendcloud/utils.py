import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """SendCloud connection settings."""

    # Add carrier specific api connection properties here
    username: str
    password: str

    @property
    def carrier_name(self):
        return "sendcloud"

    @property
    def server_url(self):
        return "https://panel.sendcloud.sc" if not self.test_mode else "https://panel.sendcloud.sc"

    @property
    def tracking_url(self):
        return "https://tracking.sendcloud.sc/track/{}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

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
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list) 
