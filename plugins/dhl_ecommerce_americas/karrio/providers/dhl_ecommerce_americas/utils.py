import attr
import base64
import typing
import karrio.core as core


@attr.s(auto_attribs=True)
class Settings(core.Settings):
    """DHL eCommerce Americas connection settings."""

    client_id: str
    password: str
    test_mode: bool = False

    carrier_id: str = "dhl_ecommerce_americas"
    account_country_code: str = "US"
    id: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "dhl_ecommerce_americas"

    @property
    def server_url(self):
        return "https://api.dhlecommerce.dhl.com"

    @property
    def authorization(self):
        return base64.b64encode(f"{self.client_id}:{self.password}".encode()).decode()

    @property
    def tracking_url(self):
        return "https://track.dhl.com/tracking?lang=en&id={}"

    @property
    def connection_config(self) -> typing.Any:
        from karrio.providers.dhl_ecommerce_americas.units import ConnectionConfig
        import karrio.lib as lib

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
