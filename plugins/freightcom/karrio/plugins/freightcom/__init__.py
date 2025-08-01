import karrio.core.metadata as metadata
import karrio.mappers.freightcom as mappers
import karrio.providers.freightcom.units as units


METADATA = metadata.PluginMetadata(
    status="deprecated",
    id="freightcom",
    label="Freightcom",
    is_hub=True,
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    options=units.ShippingOption,
    services=units.ShippingService,
    hub_carriers=units.CARRIER_IDS,
)
