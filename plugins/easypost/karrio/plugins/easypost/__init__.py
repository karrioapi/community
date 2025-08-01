import karrio.core.metadata as metadata
import karrio.mappers.easypost as mappers
import karrio.providers.easypost.units as units


METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="easypost",
    label="EasyPost",
    is_hub=True,
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    options=units.ShippingOption,
    services=units.Service,
    hub_carriers=units.CarrierId.to_dict(),
)
