import base64
import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DHL eCommerce Europe connection settings."""

    username: str
    password: str
    account_number: str = None
    test: bool = False
    shipper_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_ecommerce_europe"

    @property
    def server_url(self):
        return (
            "https://api-mock.dhl.com/mydhlapi"
            if self.test
            else "https://api-eu.dhl.com/mydhlapi"
        )

    @property
    def authorization(self):
        """Generate basic auth header."""
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    @property  
    def connection_config(self):
        from karrio.core.units import ShippingOptions
        return ShippingOptions(
            dict(
                username=self.username,
                password=self.password,
                account_number=self.account_number,
                test=self.test,
                shipper_country_code=self.shipper_country_code,
            )
        )


def request(
    url: str,
    data: typing.Union[str, dict] = None,
    trace: typing.List[typing.Tuple[str, str]] = None,
    method: str = "GET",
    settings: Settings = None,
) -> str:
    """Make HTTP request to DHL eCommerce Europe API."""
    
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
