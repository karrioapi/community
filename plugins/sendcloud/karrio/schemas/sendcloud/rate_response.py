"""SendCloud rate response schema."""

import attr
from typing import Optional, List, Dict, Any


@attr.s(auto_attribs=True)
class FunctionalitiesType:
    delivery_confirmation: Optional[bool] = None
    saturday_delivery: Optional[bool] = None
    evening_delivery: Optional[bool] = None


@attr.s(auto_attribs=True)
class ShippingProductType:
    name: Optional[str] = None
    code: Optional[str] = None
    service_point_input: Optional[str] = None
    carrier: Optional[str] = None
    price: Optional[float] = None
    selected: Optional[bool] = None
    min_weight: Optional[str] = None
    max_weight: Optional[str] = None
    countries: Optional[List[str]] = None
    methods: Optional[List[str]] = None
    status: Optional[str] = None
    functionalities: Optional[FunctionalitiesType] = None


@attr.s(auto_attribs=True)
class ResultType:
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    price: Optional[float] = None
    carrier: Optional[str] = None
    selected: Optional[bool] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    shipping_products: Optional[List[ShippingProductType]] = None
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[List[ResultType]] = None 
