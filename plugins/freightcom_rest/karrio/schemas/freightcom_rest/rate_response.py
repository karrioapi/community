import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BaseType:
    currency: typing.Optional[str] = None
    value: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class CustomsChargeDataType:
    duties_and_taxes_surcharge_keys: typing.Optional[typing.List[str]] = None
    guarantee_fee_surcharge_keys: typing.Optional[typing.List[str]] = None
    carrier_and_government_fees_surcharge_keys: typing.Optional[typing.List[str]] = None
    processing_fees_surcharge_keys: typing.Optional[typing.List[str]] = None
    is_rate_guaranteed: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class SurchargeType:
    type: typing.Optional[str] = None
    amount: typing.Optional[BaseType] = jstruct.JStruct[BaseType]


@attr.s(auto_attribs=True)
class ValidUntilType:
    year: typing.Optional[int] = None
    month: typing.Optional[int] = None
    day: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RateType:
    carrier_name: typing.Optional[str] = None
    service_name: typing.Optional[str] = None
    service_id: typing.Optional[str] = None
    valid_until: typing.Optional[ValidUntilType] = jstruct.JStruct[ValidUntilType]
    total: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    base: typing.Optional[BaseType] = jstruct.JStruct[BaseType]
    surcharges: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    taxes: typing.Optional[typing.List[SurchargeType]] = jstruct.JList[SurchargeType]
    transit_time_days: typing.Optional[int] = None
    transit_time_not_available: typing.Optional[bool] = None
    paperless: typing.Optional[bool] = None
    customs_charge_data: typing.Optional[CustomsChargeDataType] = jstruct.JStruct[CustomsChargeDataType]


@attr.s(auto_attribs=True)
class StatusType:
    done: typing.Optional[bool] = None
    total: typing.Optional[int] = None
    complete: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RateResponseType:
    status: typing.Optional[StatusType] = jstruct.JStruct[StatusType]
    rates: typing.Optional[typing.List[RateType]] = jstruct.JList[RateType]
