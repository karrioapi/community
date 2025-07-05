"""Karrio ShipEngine connection settings and utilities."""

import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors
import typing
import karrio.core.settings as settings


class Settings(settings.Settings):
    """ShipEngine connection settings with API key authentication."""

    # API Key authentication for ShipEngine
    api_key: str
    carrier_id: str = "shipengine"
    account_country_code: str = "US"
    metadata: typing.Dict = {}
    config: typing.Dict = {}
    test_mode: bool = False

    @property
    def carrier_name(self):
        """Returns the carrier name."""
        return "shipengine"

    @property
    def server_url(self):
        """Returns the API server URL.
        
        ShipEngine uses the same URL for both test and production environments.
        The API key determines the actual environment and account access.
        """
        return (
            "https://api.shipengine.com"
            if not self.test_mode
            else "https://api.shipengine.com"  # ShipEngine uses the same URL for test/prod
        )

    @property
    def tracking_url(self):
        """Returns the tracking URL template."""
        return "https://www.shipengine.com/tracking/{}"

    @property
    def authorization(self):
        """Returns the authorization header value.
        
        ShipEngine uses API key authentication in the format:
        "API-Key: {api_key}"
        
        Returns:
            str: Authorization header value
        """
        return f"API-Key {self.api_key}"

    @property
    def connection_config(self) -> lib.units.Options:
        """Returns connection configuration options."""
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def validate_api_key(api_key: str) -> bool:
    """Validate ShipEngine API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    # ShipEngine API keys typically start with "TEST_" for sandbox or have specific format
    return bool(api_key and len(api_key) >= 10)


def create_request_headers(settings: Settings) -> dict:
    """Create standard request headers for ShipEngine API.
    
    Args:
        settings: ShipEngine settings
        
    Returns:
        dict: Request headers
    """
    return {
        "API-Key": settings.api_key,
        "Content-Type": "application/json",
        "User-Agent": f"Karrio/{settings.carrier_name}",
    }


class ConnectionConfig(lib.Enum):
    """ShipEngine connection configuration options."""
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", str, "PDF")  # PDF default for labels
    warehouse_id = lib.OptionEnum("warehouse_id", str)
    carrier_id = lib.OptionEnum("carrier_id", str)


def default_request_serializer(data: dict) -> dict:
    return data


def default_response_deserializer(response: str) -> dict:
    return lib.to_dict(response)


def build_url(settings: Settings, endpoint: str, **kwargs) -> str:
    base_url = "https://api.shipengine.com/v1"
    params = "&".join([f"{k}={v}" for k, v in kwargs.items() if v is not None])
    return f"{base_url}/{endpoint}" + (f"?{params}" if params else "")


def get_auth_headers(settings: Settings) -> dict:
    return {
        "API-Key": settings.api_key,
        "Content-Type": "application/json",
    }
