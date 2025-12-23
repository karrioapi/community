import unittest
from unittest.mock import patch, ANY

import karrio.sdk as karrio
import karrio.lib as lib


class TestAmazonShippingAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_authenticate(self):
        # Create a fresh gateway without cached auth to test the login flow
        fresh_gateway = karrio.gateway["amazon_shipping"].create(
            dict(
                seller_id="SELLER_ID",
                developer_id="DEVELOPER_ID",
                mws_auth_token="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            ),
        )

        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            # Call authenticate directly on the proxy
            result = fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{fresh_gateway.settings.server_url}/authorization/v1/authorizationCode?developerId=DEVELOPER_ID&sellingPartnerId=SELLER_ID&mwsAuthToken=wJalrXUtnFEMI%2FK7MDENG%2FbPxRfiCYEXAMPLEKEY",
            )
            # Compare token returned
            self.assertEqual(parsed_response, "authorizationCode")


if __name__ == "__main__":
    unittest.main()


LoginResponse = """{
    "payload": {"authorizationCode": "authorizationCode"}
}
"""
