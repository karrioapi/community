
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """ShipEngine provider settings."""

    # ShipEngine credentials
    api_key: str
    carrier_ids: str = None  # Optional carrier filtering

    @property
    def carrier_name(self):
        return "shipengine"

    @property
    def server_url(self):
        return "https://api.shipengine.com/v1"

    @property
    def auth_headers(self):
        return {
            "API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    @property
    def preferred_carriers(self):
        """Parse carrier IDs from configuration."""
        if self.carrier_ids:
            return [c.strip() for c in self.carrier_ids.split(",")]
        return []

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

#     """uncomment the following code block to implement the oauth login."""
#     @property
#     def access_token(self):
#         """Retrieve the access_token using the client_id|client_secret pair
#         or collect it from the cache if an unexpired access_token exist.
#         """
#         cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
#         now = datetime.datetime.now() + datetime.timedelta(minutes=30)

#         auth = self.connection_cache.get(cache_key) or {}
#         token = auth.get("access_token")
#         expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

#         if token is not None and expiry is not None and expiry > now:
#             return token

#         self.connection_cache.set(cache_key, lambda: login(self))
#         new_auth = self.connection_cache.get(cache_key)

#         return new_auth["access_token"]

# """uncomment the following code block to implement the oauth login."""
# def login(settings: Settings):
#     import karrio.providers.shipengine.error as error

#     result = lib.request(
#         url=f"{settings.server_url}/oauth/token",
#         method="POST",
#         headers={"content-Type": "application/x-www-form-urlencoded"},
#         data=lib.to_query_string(
#             dict(
#                 grant_type="client_credentials",
#                 client_id=settings.client_id,
#                 client_secret=settings.client_secret,
#             )
#         ),
#     )

#     response = lib.to_dict(result)
#     messages = error.parse_error_response(response, settings)

#     if any(messages):
#         raise errors.ParsedMessagesError(messages)

#     expiry = datetime.datetime.now() + datetime.timedelta(
#         seconds=float(response.get("expires_in", 0))
#     )
#     return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """ShipEngine-specific connection configuration options."""
    # Hub-specific configurations
    preferred_carriers = lib.OptionEnum("preferred_carriers", list)
    excluded_carriers = lib.OptionEnum("excluded_carriers", list)
    default_service_codes = lib.OptionEnum("default_service_codes", list)

    # Standard configurations
    shipping_options = lib.OptionEnum("shipping_options", list)
    label_format = lib.OptionEnum("label_format", str, "PDF")
    label_size = lib.OptionEnum("label_size", str, "4x6")
