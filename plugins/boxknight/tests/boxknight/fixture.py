import datetime
import karrio.sdk as karrio
import karrio.lib as lib

expiry = datetime.datetime.now() + datetime.timedelta(days=1)
cached_auth = {
    f"boxknight|username|password": dict(
        token="****",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

gateway = karrio.gateway["boxknight"].create(
    dict(
        username="username",
        password="password",
    ),
    cache=lib.Cache(**cached_auth),
)
