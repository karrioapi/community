import karrio.core.metadata as metadata
import karrio.mappers.gls_eu.mapper as mapper
import karrio.mappers.gls_eu.proxy as proxy
import karrio.mappers.gls_eu.settings as settings
import karrio.providers.gls_eu.units as units

METADATA = metadata.PluginMetadata(
    status="beta",
    id="gls_eu",
    label="GLS EU",

    Mapper=mapper.Mapper,
    Proxy=proxy.Proxy,
    Settings=settings.Settings,

    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=units.ConnectionConfig,

    is_hub=False
)
