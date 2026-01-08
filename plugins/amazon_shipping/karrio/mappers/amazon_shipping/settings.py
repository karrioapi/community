"""Karrio Amazon Shipping connection settings."""

import attr
import karrio.providers.amazon_shipping.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Amazon Shipping SP-API connection settings.

    Credentials for Login with Amazon (LWA) OAuth2 authentication:
    - client_id: LWA application client ID
    - client_secret: LWA application client secret
    - refresh_token: LWA refresh token for the authorized seller

    Optional configuration:
    - aws_region: AWS region (us-east-1, eu-west-1, us-west-2)
    - shipping_business_id: Amazon business ID header (e.g., AmazonShipping_US)
    """

    # Required SP-API credentials
    client_id: str
    client_secret: str
    refresh_token: str

    # Optional configuration
    aws_region: str = "us-east-1"
    shipping_business_id: str = None

    # Standard karrio settings
    account_country_code: str = None
    carrier_id: str = "amazon_shipping"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
