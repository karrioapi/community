import karrio.core.metadata as metadata
import karrio.mappers.hay_post as mappers
import karrio.providers.hay_post.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="hay_post",
    label="HayPost",

    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    # Data Units
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
    # package_presets=units.PackagePresets,  # Enum of parcel presets/templates

    is_hub=False
)
