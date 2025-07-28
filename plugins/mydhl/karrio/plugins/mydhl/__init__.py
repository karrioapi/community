import karrio.core.metadata as metadata
import karrio.mappers.mydhl as mappers
import karrio.providers.mydhl.units as units
import karrio.providers.mydhl.utils as utils

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="mydhl",
    label="MyDHL Express",
    description="DHL Express MyDHL API integration for international shipping to 220+ countries and territories",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=utils.ConnectionConfig,
    package_presets=units.PackagePresets,
    packaging_types=units.DCTPackageType,
    has_intl_accounts=True,
    # Extra info
    website="https://www.dhl.com/express",
    documentation="https://developer.dhl.com/api-reference/dhl-express-mydhl-api",
) 
