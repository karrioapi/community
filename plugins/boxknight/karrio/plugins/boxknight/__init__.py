import karrio.core.metadata as metadata
import karrio.mappers.boxknight as mappers
import karrio.providers.boxknight.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="boxknight",
    label="BoxKnight",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False,
    services=units.ShippingService,
    options=units.ShippingOption,
    # New fields
    website="https://www.boxknight.com/",
    documentation="https://www.docs.boxknight.com/",
    description="Specializes in same-day delivery at affordable prices for e-commerce retailers. Our mission is to get packages to your customers when they are actually home and as quickly as possible.",
)