import karrio.core.metadata as metadata
import karrio.mappers.dhl_ecommerce_europe as mappers
import karrio.providers.dhl_ecommerce_europe.units as units
import karrio.providers.dhl_ecommerce_europe.utils as utils

METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_ecommerce_europe",
    label="DHL eCommerce Europe",
    description="DHL eCommerce Europe shipping integration for European e-commerce solutions",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.dhl.com/global-en/home/our-divisions/ecommerce-solutions.html",
    documentation="https://developer.dhl.com/api-reference/ecommerce-europe",
)
