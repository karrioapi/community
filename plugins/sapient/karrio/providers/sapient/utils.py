import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
import karrio.core.models as models


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

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,
        ).get_state()


def login(settings: Settings):
    import karrio.providers.sapient.error as error

    result = lib.request(
        url=f"https://authentication.intersoftsapient.net/connect/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Karrio/1.0",
        },
        data=lib.to_query_string(
            dict(
                grant_type="client_credentials",
                client_id=settings.client_id,
                client_secret=settings.client_secret,
            )
        ),
        on_error=parse_error_response,
    )

    # Handle case where result is a plain string (error response)
    # instead of JSON - parse_error_response may return non-JSON strings
    response = lib.failsafe(lambda: lib.to_dict(result)) or {}

    # If we couldn't parse as JSON, treat the result as an error message
    if not response and isinstance(result, str):
        response = {"error": result}

    # Handle OAuth error response format (error, error_description)
    if "error" in response:
        raise errors.ParsedMessagesError(
            messages=[
                models.Message(
                    carrier_name=settings.carrier_name,
                    carrier_id=settings.carrier_id,
                    message=response.get("error_description", response.get("error")),
                    code=response.get("error", "AUTH_ERROR"),
                )
            ]
        )

    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    # Validate that access_token is present in the response
    if "access_token" not in response:
        raise errors.ParsedMessagesError(
            messages=[
                models.Message(
                    carrier_name=settings.carrier_name,
                    carrier_id=settings.carrier_id,
                    message="Authentication failed: No access token received",
                    code="AUTH_ERROR",
                )
            ]
        )

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )
    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    service_level = lib.OptionEnum("service_level", str)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


def parse_error_response(response):
    """Parse the error response from the SAPIENT API."""
    content = lib.failsafe(lambda: lib.decode(response.read()))

    # If we have content, try to return it as-is (likely already JSON string)
    if any(content or ""):
        return content

    # If no content, create a JSON error object
    return lib.to_json(
        dict(Errors=[dict(ErrorCode=str(response.code), Message=response.reason)])
    )
