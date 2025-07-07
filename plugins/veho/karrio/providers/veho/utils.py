import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Veho connection settings."""

    api_key: str
    account_number: str = None

    @property
    def carrier_name(self):
        return "veho"

    @property
    def server_url(self):
        return (
            "https://api.shipveho.com"
            if not self.test_mode
            else "https://sandbox.api.shipveho.com"
        )

    @property
    def tracking_url(self):
        return "https://www.shipveho.com/tracking/{}"

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")
    delivery_max_datetime = lib.OptionEnum("delivery_max_datetime", str)
    label_date = lib.OptionEnum("label_date", str)
