import karrio.core.metadata as metadata
import karrio.mappers.asendia_us as mappers
import karrio.providers.asendia_us.units as units
import karrio.providers.asendia_us.utils as utils


METADATA = metadata.PluginMetadata(
    status="beta",
    id="asendia_us",
    label="Asendia US",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
    # New fields
    website="https://www.asendia.com/",
    documentation="https://a1api.asendiausa.com/swagger/index.html",
    description="deliver cross-border e-commerce solutions that are loved by your shoppers worldwide.",
)