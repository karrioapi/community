"""Karrio SendCloud connection settings and utilities."""

import base64
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """SendCloud connection settings with OAuth2 authentication."""

    # OAuth2 credentials for SendCloud API
    client_id: str
    client_secret: str
    
    @property
    def carrier_name(self):
        """Returns the carrier name."""
        return "sendcloud"

    @property
    def server_url(self):
        """Returns the API server URL.
        
        SendCloud uses the same URL for both test and production environments.
        Authentication and account context determine the actual environment.
        """
        return (
            "https://panel.sendcloud.sc"
            if not self.test_mode
            else "https://panel.sendcloud.sc"  # SendCloud uses the same URL for test/prod
        )

    @property
    def tracking_url(self):
        """Returns the tracking URL template."""
        return "https://tracktrace.sendcloud.eu/forward?carrier={}&tracking_number={}"

    @property
    def access_token(self):
        """Retrieve the access_token using OAuth2 client credentials flow.
        
        Uses caching to avoid unnecessary API calls. Token is automatically
        refreshed when it expires.
        
        Returns:
            str: Valid access token
        """
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def connection_config(self) -> lib.units.Options:
        """Returns connection configuration options."""
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def login(settings: Settings):
    """Authenticate with SendCloud API using OAuth2 client credentials flow.
    
    Args:
        settings: SendCloud settings with client credentials
        
    Returns:
        dict: Authentication response with access token and expiry
        
    Raises:
        ParsedMessagesError: If authentication fails
    """
    import karrio.providers.sendcloud.error as error

    result = lib.request(
        url=f"{settings.server_url}/api/v2/auth/token/",
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=settings.client_id,
                client_secret=settings.client_secret,
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
    """SendCloud connection configuration options."""
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")  # PDF default for labels
