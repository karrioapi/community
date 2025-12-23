"""eShipper connection settings."""

import karrio.core as core


class Settings(core.Settings):
    """eShipper connection settings."""

    principal: str
    credential: str

    @property
    def carrier_name(self):
        return "eshipper"

    @property
    def server_url(self):
        return (
            "https://uu2.eshipper.com" if self.test_mode else "https://ww2.eshipper.com"
        )
