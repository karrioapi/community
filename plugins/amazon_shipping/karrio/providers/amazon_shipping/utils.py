import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
import karrio.core.models as models


class Settings(core.Settings):
    """Amazon Shipping connection settings."""

    seller_id: str
    developer_id: str
    mws_auth_token: str
    aws_region: str = "us-east-1"

    @property
    def server_url(self):
        if self.aws_region == "eu-west-1":
            return (
                "https://sandbox.sellingpartnerapi-eu.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-eu.amazon.com"
            )
        if self.aws_region == "us-west-2":
            return (
                "https://sandbox.sellingpartnerapi-fe.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-fe.amazon.com"
            )

        return (
            "https://sandbox.sellingpartnerapi-na.amazon.com"
            if self.test_mode
            else "https://sellingpartnerapi-na.amazon.com"
        )

    @property
    def carrier_name(self):
        return "amazon_shipping"

    @property
    def access_token(self):
        """Retrieve the access_token using the seller_id|developer_id pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.carrier_name}|{self.seller_id}|{self.developer_id}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="authorizationCode",
        ).get_state()


def login(settings: Settings):
    import karrio.providers.amazon_shipping.error as error

    query = urllib.parse.urlencode(
        dict(
            developerId=settings.developer_id,
            sellingPartnerId=settings.seller_id,
            mwsAuthToken=settings.mws_auth_token,
        )
    )
    result = lib.request(
        url=f"{settings.server_url}/authorization/v1/authorizationCode?{query}",
        headers={"content-Type": "application/json"},
        method="POST",
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    # Validate that authorizationCode is present in the response payload
    authorization_code = lib.failsafe(
        lambda: response.get("payload", {}).get("authorizationCode")
    )
    if not authorization_code:
        raise errors.ParsedMessagesError(
            messages=[
                models.Message(
                    carrier_name=settings.carrier_name,
                    carrier_id=settings.carrier_id,
                    message="Authentication failed: No authorization code received",
                    code="AUTH_ERROR",
                )
            ]
        )

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {
        **response,
        "expiry": lib.fdatetime(expiry),
        "authorizationCode": authorization_code,
    }
