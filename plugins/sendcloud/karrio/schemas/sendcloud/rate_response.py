import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class BilledWeightType:
    unit: typing.Optional[str] = None
    value: typing.Optional[str] = None
    volumetric: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class CarrierType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ContractType:
    id: typing.Optional[int] = None
    clientid: typing.Optional[str] = None
    carriercode: typing.Optional[str] = None
    name: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class FunctionalitiesType:
    b2b: typing.Optional[bool] = None
    b2c: typing.Optional[bool] = None
    ers: typing.Optional[bool] = None
    size: typing.Any = None
    tyres: typing.Optional[bool] = None
    sorted: typing.Optional[bool] = None
    boxable: typing.Optional[bool] = None
    premium: typing.Optional[bool] = None
    returns: typing.Optional[bool] = None
    segment: typing.Any = None
    tracked: typing.Optional[bool] = None
    idcheck: typing.Optional[bool] = None
    incoterm: typing.Any = None
    manually: typing.Optional[bool] = None
    priority: typing.Any = None
    agecheck: typing.Any = None
    insurance: typing.Any = None
    labelless: typing.Optional[bool] = None
    lastmile: typing.Optional[str] = None
    signature: typing.Optional[bool] = None
    surcharge: typing.Optional[bool] = None
    firstmile: typing.Optional[str] = None
    multicollo: typing.Optional[bool] = None
    bulkygoods: typing.Optional[bool] = None
    formfactor: typing.Optional[str] = None
    freshgoods: typing.Optional[bool] = None
    ecodelivery: typing.Optional[bool] = None
    servicearea: typing.Optional[str] = None
    flexdelivery: typing.Optional[bool] = None
    fragilegoods: typing.Optional[bool] = None
    nonconveyable: typing.Optional[bool] = None
    dangerousgoods: typing.Optional[bool] = None
    deliverybefore: typing.Any = None
    cashondelivery: typing.Any = None
    harmonizedlabel: typing.Optional[bool] = None
    weekenddelivery: typing.Any = None
    carrierinsurance: typing.Optional[bool] = None
    deliveryattempts: typing.Any = None
    deliverydeadline: typing.Optional[str] = None
    neighbordelivery: typing.Optional[bool] = None
    customsvaluelimit: typing.Any = None
    registereddelivery: typing.Optional[bool] = None
    carrierbillingtype: typing.Any = None
    personalizeddelivery: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class MaxDimensionsType:
    length: typing.Optional[str] = None
    width: typing.Optional[str] = None
    height: typing.Optional[str] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TotalType:
    value: typing.Optional[int] = None
    currency: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class BreakdownType:
    type: typing.Optional[str] = None
    label: typing.Optional[str] = None
    price: typing.Optional[TotalType] = jstruct.JStruct[TotalType]


@attr.s(auto_attribs=True)
class PriceType:
    breakdown: typing.Optional[typing.List[BreakdownType]] = jstruct.JList[BreakdownType]
    total: typing.Optional[TotalType] = jstruct.JStruct[TotalType]


@attr.s(auto_attribs=True)
class MaxType:
    value: typing.Optional[str] = None
    unit: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class WeightType:
    min: typing.Optional[MaxType] = jstruct.JStruct[MaxType]
    max: typing.Optional[MaxType] = jstruct.JStruct[MaxType]


@attr.s(auto_attribs=True)
class QuoteType:
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    price: typing.Optional[PriceType] = jstruct.JStruct[PriceType]
    leadtime: typing.Optional[int] = None


@attr.s(auto_attribs=True)
class RequirementsType:
    fields: typing.Optional[typing.List[typing.Any]] = None
    exportdocuments: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class DatumType:
    code: typing.Optional[str] = None
    name: typing.Optional[str] = None
    carrier: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    product: typing.Optional[CarrierType] = jstruct.JStruct[CarrierType]
    functionalities: typing.Optional[FunctionalitiesType] = jstruct.JStruct[FunctionalitiesType]
    contract: typing.Optional[ContractType] = jstruct.JStruct[ContractType]
    weight: typing.Optional[WeightType] = jstruct.JStruct[WeightType]
    maxdimensions: typing.Optional[MaxDimensionsType] = jstruct.JStruct[MaxDimensionsType]
    billedweight: typing.Optional[BilledWeightType] = jstruct.JStruct[BilledWeightType]
    requirements: typing.Optional[RequirementsType] = jstruct.JStruct[RequirementsType]
    quotes: typing.Optional[typing.List[QuoteType]] = jstruct.JList[QuoteType]


@attr.s(auto_attribs=True)
class RateResponseType:
    data: typing.Optional[typing.List[DatumType]] = jstruct.JList[DatumType]
