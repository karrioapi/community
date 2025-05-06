import karrio.core.metadata as metadata
import karrio.mappers.canpar as mappers
import karrio.providers.canpar.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="canpar",
    label="Canpar",

    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

    # Data Units

    # New fields
    website="https://www.canpar.com/",
    documentation="https://www.canpar.com/en/solutions/ecommerce_tools.htm",
    description="Everything Canpar Express does-product development, technological upgrades, customer service-is shaped and tailored to transporting our customers' parcels efficiently and cost-effectively.",
)
