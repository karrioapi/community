from attr import define, field
from typing import Optional, List


@define
class TrackingRequest:
    tracking_numbers: Optional[List[str]] = None
    account_number: Optional[str] = None 
