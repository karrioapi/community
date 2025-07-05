from karrio.core.metadata import PluginMetadata

from karrio.mappers.sendcloud.mapper import Mapper
from karrio.mappers.sendcloud.proxy import Proxy
from karrio.mappers.sendcloud.settings import Settings
import karrio.providers.sendcloud.units as units
import karrio.providers.sendcloud.utils as utils

# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="sendcloud",
    label="SendCloud",
    description="SendCloud shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=False,
    # options=units.ShippingOption,
    # services=units.ShippingService,
    # Extra info
    website="",
    documentation="",
)
