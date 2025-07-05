import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class EstimatedDeliveryDate:
    earliest: typing.Optional[str] = None
    latest: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class CarrierDeliveryDays:
    monday: typing.Optional[bool] = None
    tuesday: typing.Optional[bool] = None
    wednesday: typing.Optional[bool] = None
    thursday: typing.Optional[bool] = None
    friday: typing.Optional[bool] = None
    saturday: typing.Optional[bool] = None
    sunday: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class MoneyAmount:
    currency: str
    amount: float


@attr.s(auto_attribs=True)
class Rate:
    rate_id: str
    rate_type: str
    carrier_id: str
    shipping_amount: MoneyAmount
    insurance_amount: MoneyAmount
    confirmation_amount: MoneyAmount
    other_amount: MoneyAmount
    zone: typing.Optional[int] = None
    package_type: typing.Optional[str] = None
    delivery_days: typing.Optional[int] = None
    guaranteed_service: typing.Optional[bool] = None
    estimated_delivery_date: typing.Optional[EstimatedDeliveryDate] = None
    carrier_delivery_days: typing.Optional[CarrierDeliveryDays] = None
    ship_date: typing.Optional[str] = None
    negotiated_rate: typing.Optional[bool] = None
    service_type: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    trackable: typing.Optional[bool] = None
    carrier_code: typing.Optional[str] = None
    carrier_nickname: typing.Optional[str] = None
    carrier_friendly_name: typing.Optional[str] = None
    validation_status: typing.Optional[str] = None
    warning_messages: typing.Optional[typing.List[str]] = jstruct.JList[str]
    error_messages: typing.Optional[typing.List[str]] = jstruct.JList[str]


@attr.s(auto_attribs=True)
class RateResponse:
    rate_request_id: str
    shipment_id: str
    created_at: str
    status: str
    rates: typing.List[Rate] = jstruct.JList[Rate]
    invalid_rates: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None
    rate_request_id: typing.Optional[str] = None
    shipment_id: typing.Optional[str] = None
    created_at: typing.Optional[str] = None
    status: typing.Optional[str] = None
    errors: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None 
