import karrio.core.metadata as metadata
import karrio.mappers.nationex as mappers
import karrio.providers.nationex.units as units


METADATA = metadata.PluginMetadata(
    status="beta",
    id="nationex",
    label="Nationex",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False
)