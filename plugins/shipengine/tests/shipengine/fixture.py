import karrio.sdk as karrio

gateway = karrio.gateway["shipengine"].create(
    dict(
        api_key="test_api_key",
    )
)