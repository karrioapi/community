import karrio.core.metadata as metadata
import karrio.mappers.shipengine as mappers
import karrio.providers.shipengine.units as units
import karrio.providers.shipengine.utils as utils

METADATA = metadata.Metadata(
    id="shipengine",
    label="ShipEngine",
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
