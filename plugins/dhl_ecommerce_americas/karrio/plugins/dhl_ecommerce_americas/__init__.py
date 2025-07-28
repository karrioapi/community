import karrio.core.metadata as metadata
import karrio.mappers.dhl_ecommerce_americas as mappers
import karrio.providers.dhl_ecommerce_americas.units as units
import karrio.providers.dhl_ecommerce_americas.utils as utils


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_ecommerce_americas",
    label="DHL eCommerce Americas",
    description="DHL eCommerce Americas shipping integration for North and South America",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.DHLService,
    options=units.DHLOption,
    connection_configs=utils.ConnectionConfig,
    # Extra info
    website="https://www.dhl.com/us-en/home/our-divisions/ecommerce-solutions.html",
    documentation="https://developer.dhl.com/api-reference/label-dhl-ecommerce-americas",
)
