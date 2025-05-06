import karrio.core.metadata as metadata
import karrio.mappers.tnt as mappers
import karrio.providers.tnt.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="tnt",
    label="TNT",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    packaging_types=units.PackageType,
    package_presets=units.PackagePresets,
    connection_configs=units.ConnectionConfig,
    has_intl_accounts=True,
    # New fields
    website="https://www.tnt.com",
    description="TNT is an international courier delivery services company with headquarters in the Netherlands.",
)
