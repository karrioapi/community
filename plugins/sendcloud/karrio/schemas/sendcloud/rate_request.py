"""SendCloud rate request schema."""

import attr
from typing import Optional, List


@attr.s(auto_attribs=True)
class AddressType:
    name: Optional[str] = None
    company: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None


@attr.s(auto_attribs=True)
class ParcelType:
    height: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    weight: Optional[float] = None


@attr.s(auto_attribs=True)
class ServicePointType:
    code: Optional[str] = None
    carrier: Optional[str] = None


@attr.s(auto_attribs=True)
class RateRequestType:
    from_address: Optional[AddressType] = None
    to_address: Optional[AddressType] = None
    parcels: Optional[List[ParcelType]] = None
    service_points: Optional[List[ServicePointType]] = None
    to_service_point: Optional[int] = None
    from_service_point: Optional[int] = None 
