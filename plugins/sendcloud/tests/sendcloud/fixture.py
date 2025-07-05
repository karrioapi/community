"""SendCloud carrier tests fixtures."""

import karrio.sdk as karrio
import datetime
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "test_client_id"
client_secret = "test_client_secret"

cached_auth = {
    f"sendcloud|{client_id}|{client_secret}": dict(
        access_token="test_access_token",
        token_type="bearer",
        expires_in=3600,
        scope="api",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    ),
}

gateway = karrio.gateway["sendcloud"].create(
    dict(
        client_id=client_id,
        client_secret=client_secret,
        account_country_code="NL",
    ),
    cache=lib.Cache(**cached_auth),
)
