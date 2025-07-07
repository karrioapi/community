from karrio.mappers.sendcloud.mapper import Mapper
from karrio.mappers.sendcloud.proxy import Proxy
from karrio.mappers.sendcloud.settings import Settings

# Define METADATA here to avoid circular imports
from karrio.core.metadata import Metadata as PluginMetadata
import karrio.providers.sendcloud.units as units
import karrio.providers.sendcloud.utils as utils

METADATA = PluginMetadata(
    id="sendcloud",
    label="SendCloud",
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    is_hub=True,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)