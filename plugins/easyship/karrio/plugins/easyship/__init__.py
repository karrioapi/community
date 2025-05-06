import karrio.core.metadata as metadata
import karrio.mappers.easyship as mappers
import karrio.providers.easyship.units as units
import karrio.providers.easyship.utils as utils


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="easyship",
    label="Easyship",
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
