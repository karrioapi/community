from karrio.core.metadata import Metadata

from karrio.mappers.nationex.mapper import Mapper
from karrio.mappers.nationex.proxy import Proxy
from karrio.mappers.nationex.settings import Settings
import karrio.providers.nationex.units as units


METADATA = Metadata(
    status="beta",
    id="nationex",
    label="Nationex",
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    is_hub=False
)
