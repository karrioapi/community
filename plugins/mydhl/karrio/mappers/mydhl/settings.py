import attr
import karrio.lib as lib

@attr.s(auto_attribs=True)
class Settings(lib.Settings):
    username: str
    password: str
    account_number: str = None
    
    @property
    def carrier_name(self):
        return "mydhl"
    
    @property
    def server_url(self):
        return "https://express.api.dhl.com"
