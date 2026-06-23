"""Freightcom Rest carrier tests fixtures."""

import karrio.sdk as karrio
import karrio.lib as lib

cached_payment_method_id = {
    f"payment|freightcom_rest|net_terms|TEST_API_KEY": dict(
        id="string",
        type= "net-terms",
        label="Net Terms"
    )
}
gateway = karrio.gateway["freightcom_rest"].create(
    dict(
        api_key="TEST_API_KEY",
        config=dict(
            payment_method_type="net_terms"
        ),
    ),
    cache=lib.Cache(**cached_payment_method_id),

)
