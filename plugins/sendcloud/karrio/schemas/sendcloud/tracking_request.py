"""SendCloud tracking request schema."""

import attr
from typing import Optional


@attr.s(auto_attribs=True)
class TrackingRequestType:
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    postal_code: Optional[str] = None 
