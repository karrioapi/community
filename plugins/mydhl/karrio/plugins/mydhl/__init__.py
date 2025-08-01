import karrio.core.metadata as metadata
import karrio.mappers.mydhl as mappers
import karrio.providers.mydhl.units as units
import karrio.providers.mydhl.utils as utils

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="mydhl",
    label="MyDHL Express",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=utils.ConnectionConfig,
)
