import unittest
from unittest.mock import patch, ANY

import karrio.sdk as karrio
import karrio.lib as lib


class TestLocate2uAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_authenticate(self):
        # Create a fresh gateway without cached auth to test the login flow
        fresh_gateway = karrio.gateway["locate2u"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
            ),
        )

        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            # Call authenticate directly on the proxy
            result = fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{fresh_gateway.settings.auth_server_url}/connect/token",
            )
            # Compare token returned
            self.assertEqual(parsed_response, "access_token")

    def test_parse_error_response(self):
        # Create a fresh gateway without cached auth to test the login flow
        fresh_gateway = karrio.gateway["locate2u"].create(
            dict(
                client_id="client_id",
                client_secret="client_secret",
            ),
        )

        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                fresh_gateway.proxy.authenticate()


if __name__ == "__main__":
    unittest.main()


ParsedLoginResponse = {
    "expiry": ANY,
    "token_type": "Bearer",
    "access_token": "access_token",
    "scope": "locate2u.api",
    "expires_in": 3600,
}

LoginResponse = """{
  "access_token": "access_token",
  "expires_in": 3600,
  "token_type": "Bearer",
  "scope": "locate2u.api"
}
"""

ErrorResponse = """{
    "error": "invalid_client"
}
"""
