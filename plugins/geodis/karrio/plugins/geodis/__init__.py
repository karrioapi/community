import karrio.core.metadata as metadata
import karrio.mappers.geodis as mappers
import karrio.providers.geodis.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="geodis",
    label="GEODIS",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=units.ConnectionConfig,
    service_levels=units.DEFAULT_SERVICES,
)
