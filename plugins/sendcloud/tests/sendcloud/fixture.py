"""SendCloud carrier tests fixtures."""

import karrio.sdk as karrio

gateway = karrio.gateway["sendcloud"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="sendcloud",
        client_id="test_client_id",
        client_secret="test_client_secret",
    )
)
