import karrio.core.metadata as metadata
import karrio.mappers.eshipper as mappers
import karrio.providers.eshipper.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="eshipper",
    label="eShipper",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=True,
    services=units.ShippingService,
    options=units.ShippingOption,
)
