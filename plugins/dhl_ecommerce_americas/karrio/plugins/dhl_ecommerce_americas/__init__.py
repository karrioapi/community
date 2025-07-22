import karrio.core.metadata as metadata
import karrio.providers.dhl_ecommerce_americas.units as units
import karrio.providers.dhl_ecommerce_americas.utils as utils

from karrio.mappers.dhl_ecommerce_americas.mapper import Mapper
from karrio.mappers.dhl_ecommerce_americas.proxy import Proxy
from karrio.mappers.dhl_ecommerce_americas.settings import Settings


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_ecommerce_americas",
    label="DHL eCommerce Americas",
    description="DHL eCommerce Americas shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    services=units.DHLService,
    options=units.DHLOption,
    connection_configs=units.ConnectionConfig,
    # Extra info
    website="https://www.dhl.com",
    documentation="https://developer.dhl.com",
)
