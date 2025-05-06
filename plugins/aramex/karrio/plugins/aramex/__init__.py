import karrio.core.metadata as metadata
import karrio.mappers.aramex as mappers
# import karrio.providers.aramex.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="aramex",
    label="Aramex",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    # options=units.OptionCode,
    # package_presets=units.PackagePresets,
    # packaging_types=units.PackagingType,
    # services=units.Serives,
    has_intl_accounts=True,
    # New fields
    website="https://www.aramex.com/ae/en",
    documentation="https://www.aramex.com/us/en/developers-solution-center/aramex-apis",
    description="Aramex is the leading global logistics provider.",
)
