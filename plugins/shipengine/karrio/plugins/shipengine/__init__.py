from karrio.core.metadata import PluginMetadata

from karrio.mappers.shipengine.mapper import Mapper
from karrio.mappers.shipengine.proxy import Proxy
from karrio.mappers.shipengine.settings import Settings
import karrio.providers.shipengine.units as units
import karrio.providers.shipengine.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="shipengine",
    label="ShipEngine",
    description="ShipEngine multi-carrier shipping platform integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=True,  # 🔑 KEY: Hub carrier flag
    options=units.ShippingOption,
    services=units.ShippingService,  # Dynamic services
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.shipengine.com",
    documentation="https://www.shipengine.com/docs/",
)
