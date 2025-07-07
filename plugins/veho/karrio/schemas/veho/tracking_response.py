from attr import define, field
from typing import Optional, List


@define
class TrackingEvent:
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


@define
class TrackingInfo:
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    delivered: Optional[bool] = None
    delivery_date: Optional[str] = None
    events: Optional[List[TrackingEvent]] = None


@define
class TrackingResponse:
    tracking_info: Optional[List[TrackingInfo]] = None
    errors: Optional[List[str]] = None 
