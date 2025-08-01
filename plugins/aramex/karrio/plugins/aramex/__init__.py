import karrio.core.metadata as metadata
import karrio.mappers.aramex as mappers


METADATA = metadata.PluginMetadata(
    status="beta",
    id="aramex",
    label="Aramex",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    has_intl_accounts=True,
    website="https://www.aramex.com/ae/en",
    documentation="https://www.aramex.com/us/en/developers-solution-center/aramex-apis",
    description="Aramex is the leading global logistics provider.",
)
