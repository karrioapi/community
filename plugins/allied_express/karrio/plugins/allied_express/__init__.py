import karrio.core.metadata as metadata
import karrio.mappers.allied_express as mappers
import karrio.providers.allied_express.units as units
import karrio.providers.allied_express.utils as utils


METADATA = metadata.PluginMetadata(
    status="beta",
    id="allied_express",
    label="Allied Express",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    connection_configs=utils.ConnectionConfig,
)
