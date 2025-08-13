from karrio.core.metadata import PluginMetadata

from karrio.mappers.freightcom_rest.mapper import Mapper
from karrio.mappers.freightcom_rest.proxy import Proxy
from karrio.mappers.freightcom_rest.settings import Settings
import karrio.providers.freightcom_rest.units as units
import karrio.providers.freightcom_rest.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = PluginMetadata(
    id="freightcom_rest",
    label="Freightcom Rest",
    description="Freightcom Rest shipping integration for Karrio",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Data Units
    is_hub=True,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.freightcom.com/",
    documentation="https://developer.freightcom.com/",
)
