import attr
import karrio.providers.gls_eu.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """GLS EU connection settings."""

    pass 