"""SendCloud tracking response schema."""

import attr
from typing import Optional, List


@attr.s(auto_attribs=True)
class TrackingEventType:
    timestamp: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    location: Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingType:
    code: Optional[str] = None
    tracking_number: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    updated: Optional[str] = None
    carrier: Optional[str] = None
    tracking_events: Optional[List[TrackingEventType]] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    tracking: Optional[TrackingType] = None 
