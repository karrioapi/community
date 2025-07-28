"""SendCloud provider utility functions for API v2/v3"""
import base64
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.utils as utils
import karrio.core.errors as errors
import karrio.core.settings as settings
import datetime
import urllib.parse


class Settings(settings.Settings):
    """SendCloud API v2/v3 connection settings."""
    
    # API credentials
    client_id: str
    client_secret: str
    
    # Optional settings
    sender_address_id: int = None  # Default sender address ID
    test_mode: bool = False
    
    # Base properties
    id: str = None
    account_country_code: str = "NL"
    metadata: dict = {}
    config: dict = {}
    
    @property
    def carrier_name(self):
        return "sendcloud"

    @property
    def server_url(self):
        """Get the SendCloud API server URL."""
        return "https://panel.sendcloud.sc"
    
    @property
    def api_url(self):
        return f"{self.server_url}/api/v2"
    
    @property
    def tracking_url(self):
        """Get the tracking URL template."""
        return "https://tracking.sendcloud.sc/forward"
    
    @property
    def access_token(self):
        if not all([self.client_id, self.client_secret]):
            raise Exception(
                "The client_id and client_secret are required for SendCloud API requests."
            )

        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.client_id,
                client_secret=self.client_secret,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def connection_config(self) -> lib.units.Options:
        """Get connection configuration for API requests."""
        return lib.units.Options(
            {
                "url": self.server_url,
                "headers": {
                    "Authorization": f"Basic {self._get_auth_header()}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": f"karrio/{lib.__version__}",
                },
                "timeout": 120,
            }
        )
    
    def _get_auth_header(self) -> str:
        """Generate Basic Auth header for SendCloud API."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return encoded_credentials


def standard_request_serializer(
    serializer: typing.Callable=lib.identity,
) -> typing.Callable[[str], str]:
    """Standard serializer for SendCloud requests."""

    def _serialize(data: str) -> str:
        return serializer(data)

    return _serialize


def default_request_serializer(data: dict) -> dict:
    return data


def default_response_deserializer(response: str) -> dict:
    return lib.to_dict(response)


def build_url(settings: Settings, endpoint: str, **kwargs) -> str:
    base_url = settings.api_url
    params = "&".join([f"{k}={v}" for k, v in kwargs.items() if v is not None])
    return f"{base_url}/{endpoint}" + (f"?{params}" if params else "")


def get_parcel_endpoint(parcel_id: str=None) -> str:
    """Get the parcels endpoint."""
    if parcel_id:
        return f"parcels/{parcel_id}"
    return "parcels"


def get_shipping_methods_endpoint() -> str:
    """Get the shipping methods endpoint."""
    return "shipping_methods"


def get_tracking_endpoint(tracking_number: str) -> str:
    """Get the tracking endpoint."""
    # SendCloud tracking is typically done via the tracking URL, not API
    return f"parcels?tracking_number={tracking_number}"


def parse_tracking_number(tracking_data: dict) -> typing.Optional[str]:
    """Extract tracking number from SendCloud response."""
    if isinstance(tracking_data, dict):
        return tracking_data.get('tracking_number')
    return None


def parse_tracking_url(tracking_data: dict) -> typing.Optional[str]:
    """Extract tracking URL from SendCloud response."""
    if isinstance(tracking_data, dict):
        return tracking_data.get('tracking_url')
    return None


def format_address_for_sendcloud(address) -> dict:
    """Format address for SendCloud API."""
    return {
        "name": address.person_name or f"{address.first_name or ''} {address.last_name or ''}".strip(),
        "company_name": address.company_name,
        "address": address.street_name or address.address_line,
        "house_number": address.street_number or "1",
        "address_2": address.address_line2,
        "city": address.city,
        "postal_code": address.postal_code,
        "country": address.country_code,
        "country_state": address.state_code,
        "email": address.email,
        "telephone": address.phone_number,
    }


def format_weight(weight: units.Weight) -> str:
    """Format weight for SendCloud API (expects string in kg)."""
    if weight is None:
        return "0.5"  # Default weight
    
    # Convert to kg if needed
    weight_kg = weight.value
    if weight.unit.lower() in ['g', 'gram', 'grams']:
        weight_kg = weight.value / 1000
    elif weight.unit.lower() in ['lb', 'lbs', 'pound', 'pounds']:
        weight_kg = weight.value * 0.453592
    elif weight.unit.lower() in ['oz', 'ounce', 'ounces']:
        weight_kg = weight.value * 0.0283495
    
    return str(round(weight_kg, 3))


def format_dimensions(length: units.Dimension, width: units.Dimension, height: units.Dimension) -> tuple:
    """Format dimensions for SendCloud API (expects strings in cm)."""

    def to_cm(dimension: units.Dimension) -> str:
        if dimension is None:
            return "10"  # Default size
        
        value_cm = dimension.value
        if dimension.unit.lower() in ['m', 'meter', 'meters']:
            value_cm = dimension.value * 100
        elif dimension.unit.lower() in ['mm', 'millimeter', 'millimeters']:
            value_cm = dimension.value / 10
        elif dimension.unit.lower() in ['in', 'inch', 'inches']:
            value_cm = dimension.value * 2.54
        elif dimension.unit.lower() in ['ft', 'feet', 'foot']:
            value_cm = dimension.value * 30.48
        
        return str(round(value_cm, 1))
    
    return to_cm(length), to_cm(width), to_cm(height)


def get_auth_headers(settings: Settings) -> dict:
    return {
        "Authorization": f"Bearer {settings.access_token}",
        "Content-Type": "application/json",
    }


def download_label(label_url: str) -> str:
    if not label_url:
        return None
    
    try:
        response = lib.request(url=label_url, method="GET")
        return response.decode() if isinstance(response, bytes) else response
    except Exception:
        return None


def login(settings: Settings, client_id: str=None, client_secret: str=None):
    result = lib.request(
        url=f"{settings.server_url}/api/v2/auth/token",
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=client_id,
                client_secret=client_secret,
            )
        ),
    )

    response = lib.to_dict(result)
    
    # Check for errors without circular import
    if "error" in response:
        raise Exception(f"Authentication failed: {response['error']}")

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}
