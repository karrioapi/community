import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Sendcloud connection settings."""

    public_key: str
    secret_key: str

    @property
    def carrier_name(self):
        return "sendcloud"

    @property
    def server_url(self):
        return "https://panel.sendcloud.sc/api/v2"

    @property
    def tracking_url(self):
        return "https://panel.sendcloud.sc/c/shipping/v2/track/{}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.public_key, self.secret_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
