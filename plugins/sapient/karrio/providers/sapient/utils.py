import karrio.lib as lib
import karrio.core as core


SapientCarrierCode = lib.units.create_enum(
    "SapientCarrierCode",
    ["DX", "EVRI", "RM", "UPS", "YODEL"],
)


class Settings(core.Settings):
    """SAPIENT connection settings."""

    # Add carrier specific api connection properties here
    client_id: str
    client_secret: str
    shipping_account_id: str
    sapient_carrier_code: SapientCarrierCode = "RM"  # type: ignore

    @property
    def carrier_name(self):
        return "sapient"

    @property
    def server_url(self):
        return "https://api.intersoftsapient.net"

    # """uncomment the following code block to expose a carrier tracking url."""
    # @property
    # def tracking_url(self):
    #     return "https://www.carrier.com/tracking?tracking-id={}"

    # """uncomment the following code block to implement the Basic auth."""
    # @property
    # def authorization(self):
    #     pair = "%s:%s" % (self.username, self.password)
    #     return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    service_level = lib.OptionEnum("service_level", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
