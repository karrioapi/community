"""Karrio Amazon Shipping connection settings."""

import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """Amazon Shipping SP-API connection settings.

    Amazon Shipping V2 API requires SP-API OAuth2 authentication.
    The access token is obtained through the LWA (Login with Amazon) flow.
    """

    # SP-API credentials
    client_id: str  # LWA client ID
    client_secret: str  # LWA client secret
    refresh_token: str  # LWA refresh token for offline access

    # Optional settings
    aws_region: str = "us-east-1"  # AWS region for SP-API endpoint
    shipping_business_id: str = None  # x-amzn-shipping-business-id header

    @property
    def carrier_name(self):
        return "amazon_shipping"

    @property
    def server_url(self):
        """Get the SP-API endpoint based on AWS region."""
        region_mapping = {
            # North America
            "us-east-1": "https://sellingpartnerapi-na.amazon.com",
            # Europe
            "eu-west-1": "https://sellingpartnerapi-eu.amazon.com",
            # Far East
            "us-west-2": "https://sellingpartnerapi-fe.amazon.com",
        }
        base_url = region_mapping.get(self.aws_region, region_mapping["us-east-1"])

        if self.test_mode:
            return base_url.replace("sellingpartnerapi", "sandbox.sellingpartnerapi")

        return base_url

    @property
    def token_url(self):
        """LWA token endpoint."""
        return "https://api.amazon.com/auth/o2/token"

    @property
    def connection_config(self) -> lib.units.Options:
        """Additional connection configuration."""
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    """Amazon Shipping connection configuration options."""

    shipping_business_id = lib.OptionEnum("shipping_business_id")
    label_format = lib.OptionEnum("label_format", str)
    label_size_width = lib.OptionEnum("label_size_width", float)
    label_size_length = lib.OptionEnum("label_size_length", float)
    label_size_unit = lib.OptionEnum("label_size_unit", str)
