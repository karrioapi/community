import karrio.core.metadata as metadata
import karrio.mappers.sendcloud as mappers
import karrio.providers.sendcloud.units as units
import karrio.providers.sendcloud.utils as utils

METADATA = metadata.Metadata(
    id="sendcloud",
    label="SendCloud",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=True,
    options=units.ShippingOption,
    services=units.ShippingService,
    connection_configs=utils.ConnectionConfig,
) 
