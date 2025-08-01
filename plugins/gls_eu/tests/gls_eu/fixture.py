"""GLS EU carrier tests fixtures."""

import karrio.sdk as karrio

gateway = karrio.gateway["gls_eu"].create(
    dict(
        username="test_username",
        password="test_password",
        customer_id="2760",
        test_mode=True,
        carrier_id="gls_eu",
    )
) 
