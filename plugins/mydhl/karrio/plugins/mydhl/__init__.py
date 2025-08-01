import karrio.core.metadata as metadata
import karrio.mappers.mydhl as mappers

METADATA = metadata.PluginMetadata(
    status="production-ready",
    id="mydhl",
    label="MyDHL Express",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    is_hub=False,
)
