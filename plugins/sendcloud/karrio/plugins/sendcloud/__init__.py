import karrio.core.metadata as metadata
import karrio.mappers.sendcloud as mappers
import karrio.providers.sendcloud.units as units
import karrio.providers.sendcloud.utils as utils

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="sendcloud",
    label="Sendcloud",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)
