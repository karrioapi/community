"""BoxKnight connection settings."""

import karrio.core as core


class Settings(core.Settings):
    """BoxKnight connection settings."""

    username: str
    password: str

    @property
    def carrier_name(self):
        return "boxknight"

    @property
    def server_url(self):
        return "https://api.boxknight.com/v1"

    @property
    def tracking_url(self):
        return "https://www.tracking.boxknight.com/tracking?trackingNo={}"
