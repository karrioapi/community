import karrio.core.metadata as metadata
import karrio.mappers.locate2u as mappers
import karrio.providers.locate2u.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="locate2u",
    label="Locate2u",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    service_levels=units.DEFAULT_SERVICES,
)
