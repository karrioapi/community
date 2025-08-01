import karrio.core.metadata as metadata
import karrio.mappers.dhl_ecommerce_americas as mappers
import karrio.providers.dhl_ecommerce_americas.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_ecommerce_americas",
    label="DHL eCommerce Americas",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
)
