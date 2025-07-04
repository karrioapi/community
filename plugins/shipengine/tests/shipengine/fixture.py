"""ShipEngine carrier tests fixtures."""

import karrio.sdk as karrio

gateway = karrio.gateway["shipengine"].create(
    dict(
        id="123456789",
        test_mode=True,
        carrier_id="shipengine",
        api_key="test_api_key",
    )
)
