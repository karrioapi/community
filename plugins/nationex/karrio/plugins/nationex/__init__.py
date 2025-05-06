import karrio.core.metadata as metadata
import karrio.mappers.nationex as mappers
import karrio.providers.nationex.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="nationex",
    label="Nationex",
    # Integrations
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Data Units
    is_hub=False
)