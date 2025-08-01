import attr
import typing


@attr.s(auto_attribs=True)
class TrackingEvent:
    """Veho Tracking Event structure"""
    
    date: typing.Optional[str] = None
    time: typing.Optional[str] = None
    code: typing.Optional[str] = None
    description: typing.Optional[str] = None
    location: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingInfo:
    """Veho Tracking Info structure"""
    
    trackingNumber: typing.Optional[str] = None
    status: typing.Optional[str] = None
    statusDetails: typing.Optional[str] = None
    estimatedDelivery: typing.Optional[str] = None
    events: typing.Optional[typing.List[TrackingEvent]] = None


@attr.s(auto_attribs=True)
class TrackingResponse:
    """Veho Tracking Response containing trackingInfo array"""
    
    trackingInfo: typing.Optional[typing.List[TrackingInfo]] = None
