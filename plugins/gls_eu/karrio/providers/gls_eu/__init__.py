import karrio.core.metadata as metadata
import karrio.mappers.gls_eu as mappers
import karrio.providers.gls_eu.units as units

METADATA = metadata.PluginMetadata(
    status="beta",
    id="gls_eu",
    label="GLS EU",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
) 
