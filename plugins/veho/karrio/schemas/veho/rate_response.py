"""
Veho Rate Response Schema matching test data structure
"""

import attr
import typing


@attr.s(auto_attribs=True)
class RateItem:
    """Veho Rate Item - matches test API structure"""
    
    serviceCode: typing.Optional[str] = None
    serviceName: typing.Optional[str] = None
    totalCharge: typing.Optional[float] = None
    currency: typing.Optional[str] = "USD"
    transitDays: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RateResponse:
    """Veho Rate Response containing rates array"""
    
    rates: typing.Optional[typing.List[RateItem]] = None
