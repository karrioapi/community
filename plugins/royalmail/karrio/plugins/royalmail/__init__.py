import karrio.core.metadata as metadata
import karrio.mappers.royalmail as mappers


METADATA = metadata.PluginMetadata(
    status="beta",
    id="royalmail",
    label="Royal Mail",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

)
