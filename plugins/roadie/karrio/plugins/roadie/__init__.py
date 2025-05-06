import karrio.core.metadata as metadata
import karrio.mappers.roadie as mappers
import karrio.providers.roadie.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="roadie",
    label="Roadie",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
)
