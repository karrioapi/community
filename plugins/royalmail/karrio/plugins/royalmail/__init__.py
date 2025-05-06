import karrio.core.metadata as metadata
import karrio.mappers.royalmail as mappers
# import karrio.providers.royalmail.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="royalmail",
    label="Royal Mail",

    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    # Data Units
    # options=units.OptionCode,
    # package_presets=units.PackagePresets,
    # packaging_types=units.PackagingType,
    # services=units.Serives,
)
