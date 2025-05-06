import karrio.core.metadata as metadata
import karrio.mappers.sapient as mappers
import karrio.providers.sapient.units as units
import karrio.providers.sapient.utils as utils


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="sapient",
    label="SAPIENT",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=True,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
)