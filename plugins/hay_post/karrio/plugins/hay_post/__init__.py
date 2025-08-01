import karrio.core.metadata as metadata
import karrio.mappers.hay_post as mappers
import karrio.providers.hay_post.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="hay_post",
    label="HayPost",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
)
