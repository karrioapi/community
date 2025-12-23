"""Amazon Shipping connection settings."""

import karrio.core as core


class Settings(core.Settings):
    """Amazon Shipping connection settings."""

    seller_id: str
    developer_id: str
    mws_auth_token: str
    aws_region: str = "us-east-1"

    @property
    def server_url(self):
        if self.aws_region == "eu-west-1":
            return (
                "https://sandbox.sellingpartnerapi-eu.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-eu.amazon.com"
            )
        if self.aws_region == "us-west-2":
            return (
                "https://sandbox.sellingpartnerapi-fe.amazon.com"
                if self.test_mode
                else "https://sellingpartnerapi-fe.amazon.com"
            )

        return (
            "https://sandbox.sellingpartnerapi-na.amazon.com"
            if self.test_mode
            else "https://sellingpartnerapi-na.amazon.com"
        )

    @property
    def carrier_name(self):
        return "amazon_shipping"
