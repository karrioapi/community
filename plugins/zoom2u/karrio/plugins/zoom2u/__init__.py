import karrio.core.metadata as metadata
import karrio.mappers.zoom2u as mappers
import karrio.providers.zoom2u.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="zoom2u",
    label="Zoom2u",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)

