import karrio.lib as lib
import karrio.core.units as units

PRESET_DEFAULTS = dict(
    dimension_unit="CM",
    weight_unit="KG",
)

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_kg=0.01,
    min_cm=0.01,
)


class PackagePresets(lib.Enum):
    """
    Note that dimensions are in CM and weight in KG
    """
    gls_eu_envelope = lib.units.PackagePreset(
        **dict(width=35.0, height=27.5, length=1.0), **PRESET_DEFAULTS
    )
    gls_eu_small_parcel = lib.units.PackagePreset(
        **dict(width=30.0, height=20.0, length=10.0), **PRESET_DEFAULTS
    )
    gls_eu_medium_parcel = lib.units.PackagePreset(
        **dict(width=40.0, height=30.0, length=20.0), **PRESET_DEFAULTS
    )
    gls_eu_large_parcel = lib.units.PackagePreset(
        **dict(width=60.0, height=40.0, length=30.0), **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
    PDF = ("PDF", "A4")
    PNG = ("PNG", "A6")
    ZPL = ("ZPL", "4x6")

    """ Unified Label type mapping """
    pdf = PDF
    png = PNG
    zpl = ZPL


class PaymentType(lib.StrEnum):
    sender = "Sender"
    recipient = "Recipient"
    third_party = "ThirdParty"


class WeightUnit(lib.StrEnum):
    """GLS EU specific weight unit"""
    KG = "kg"
    G = "g"


class DimensionUnit(lib.StrEnum):
    """GLS EU specific dimension unit"""
    CM = "cm"
    MM = "mm"


class PackagingType(lib.StrEnum):
    """GLS EU specific packaging type"""
    PARCEL = "parcel"
    ENVELOPE = "envelope"
    PACKAGE = "package"

    """ Unified Packaging type mapping """
    envelope = ENVELOPE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", LabelType)


class ShippingService(lib.StrEnum):
    """GLS EU shipping services"""
    gls_eu_business_parcel = "Business Parcel"
    gls_eu_express = "Express"
    gls_eu_flex_delivery_service = "Flex Delivery Service"
    gls_eu_shop_delivery = "Shop Delivery"
    gls_eu_guaranteed24 = "Guaranteed24"
    gls_eu_guaranteed24_express = "Guaranteed24 Express"


class ShippingOption(lib.Enum):
    """GLS EU specific shipping options."""
    
    gls_eu_cash_on_delivery = lib.OptionEnum("cash_on_delivery", float)
    gls_eu_insurance = lib.OptionEnum("insurance", float)
    gls_eu_delivery_notification = lib.OptionEnum("delivery_notification", bool)
    gls_eu_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    gls_eu_shop_delivery = lib.OptionEnum("shop_delivery", bool)
    gls_eu_delivery_time = lib.OptionEnum("delivery_time", str)
    gls_eu_pickup_service = lib.OptionEnum("pickup_service", bool)
    gls_eu_flex_delivery = lib.OptionEnum("flex_delivery", bool)
    gls_eu_guaranteed24 = lib.OptionEnum("guaranteed24", bool)
    gls_eu_express_service = lib.OptionEnum("express_service", bool)

    """Unified Option type mapping"""
    insurance = gls_eu_insurance
    cash_on_delivery = gls_eu_cash_on_delivery
    saturday_delivery = gls_eu_saturday_delivery


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions=None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = ["PREPARED", "COLLECTED", "IN_DEPOT"]
    delivered = ["DELIVERED", "FINAL_DELIVERY"]
    in_transit = ["IN_TRANSIT", "FORWARDED", "CUSTOMS_CLEARANCE"]
    delivery_failed = ["DELIVERY_FAILED", "DAMAGED", "LOST"]
    delivery_delayed = ["DELAYED", "EXCEPTION"]
    out_for_delivery = ["OUT_FOR_DELIVERY", "WITH_DELIVERY_COURIER"]
    ready_for_pickup = ["READY_FOR_PICKUP", "DEPOT_PICKUP"]


# Legacy aliases for backward compatibility
GLSEUService = ShippingService
GLSEUOption = ShippingOption
ServiceType = ShippingService
LabelFormat = LabelType
