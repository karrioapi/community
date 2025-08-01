import karrio.core.metadata as metadata
import karrio.mappers.chronopost as mappers
from karrio.providers.chronopost import units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="chronopost",
    label="Chronopost",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    services=units.ShippingService,
    options=units.ShippingOption,
    website="https://www.chronopost.fr/en",
    documentation="https://www.chrono-api.fr/docs/api/",
    description="Provides express shipping and delivery service both domestically and internationally.",
)
