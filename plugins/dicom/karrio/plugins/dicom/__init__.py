import karrio.core.metadata as metadata
import karrio.mappers.dicom as mappers


METADATA = metadata.PluginMetadata(
    status="beta",
    id="dicom",
    label="Dicom",

    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,

)
