import karrio.core.metadata as metadata
import karrio.mappers.mydhl as mappers
import karrio.providers.mydhl.units as units
import karrio.providers.mydhl.utils as utils


# This METADATA object is used by Karrio to discover and register this plugin
# when loaded through Python entrypoints or local plugin directories.
# The entrypoint is defined in pyproject.toml under [project.entry-points."karrio.plugins"]
METADATA = metadata.Metadata(
    id="mydhl",
    label="MyDHL",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    options=units.ShippingOption,
    services=units.ShippingService,
    package_presets=units.PackagePresets,
    packaging_types=units.PackagingType,
    connection_configs=utils.ConnectionConfig,
)