import base64
import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DHL Express connection settings."""

    username: str
    password: str
    account_number: str = None
    test_mode: bool = False
    
    carrier_id: str = "dhl_express"

    @property
    def carrier_name(self):
        return "dhl_express"

    @property
    def server_url(self):
        return (
            "https://express-api-eu.dhl.com"
            if not self.test_mode
            else "https://express-api-eu.dhl.com/mydhlapi/test"
        )

    @property
    def authorization(self):
        """Generate basic auth header."""
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_express.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def request(
    url: str,
    data: typing.Union[str, dict] = None,
    trace: typing.List[typing.Tuple[str, str]] = None,
    method: str = "GET",
    settings: Settings = None,
) -> str:
    """Make HTTP request to DHL Express API."""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {settings.authorization}",
        "Accept": "application/json",
    }
    
    return lib.request(
        url=url,
        data=lib.to_json(data) if isinstance(data, dict) else data,
        trace=trace,
        method=method,
        headers=headers,
    )
