import karrio.core.metadata as metadata
import karrio.mappers.dhl_express as mappers
import karrio.providers.dhl_express.units as units
import karrio.providers.dhl_express.utils as utils


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_express",
    label="DHL Express",
    description="DHL Express MyDHL API shipping integration for Karrio",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,
    website="https://www.dhl.com",
    documentation="https://developer.dhl.com/api-reference/dhl-express-mydhl-api",
)
