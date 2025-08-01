import karrio.core.metadata as metadata
import karrio.mappers.veho as mappers
import karrio.providers.veho.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="veho",
    label="Veho",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
)
