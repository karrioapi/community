import base64
import datetime
import typing
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Sendcloud connection settings."""

    public_key: str
    secret_key: str

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "sendcloud"

    @property
    def server_url(self):
        return (
            "https://panel.sendcloud.sc/api/v2"
            if not self.test_mode
            else "https://panel.sendcloud.sc/api/v2"
        )

    @property
    def tracking_url(self):
        return "https://panel.sendcloud.sc/c/shipping/v2/track/{}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.public_key, self.secret_key)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.sendcloud.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def default_currency(self) -> typing.Optional[str]:
        return lib.units.CountryCurrency.map(self.account_country_code).value

    @property
    def access_token(self):
        """Retrieve the access_token using the public_key|secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        if not all([self.public_key, self.secret_key]):
            raise Exception(
                "The public_key and secret_key are required for Sendcloud API requests."
            )

        cache_key = f"{self.carrier_name}|{self.public_key}|{self.secret_key}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.public_key,
                client_secret=self.secret_key,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]


def login(settings: Settings, client_id: str = None, client_secret: str = None):
    """OAuth2 login function for Sendcloud API."""
    import karrio.providers.sendcloud.error as error

    result = lib.request(
        url="https://api.sendcloud.dev/auth/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=client_id,
                client_secret=client_secret,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 3600))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """Carrier specific connection configs"""

    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
