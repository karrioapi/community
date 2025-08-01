import karrio.core.metadata as metadata
import karrio.mappers.tge as mappers
import karrio.providers.tge.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="tge",
    label="TGE",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
)
