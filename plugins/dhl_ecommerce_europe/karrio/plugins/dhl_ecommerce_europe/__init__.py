import karrio.core.metadata as metadata
import karrio.mappers.dhl_ecommerce_europe as mappers
import karrio.providers.dhl_ecommerce_europe.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dhl_ecommerce_europe",
    label="DHL eCommerce Europe",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
)
