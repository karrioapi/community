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
    mydhl_express_envelope = lib.units.PackagePreset(
        **dict(width=35.0, height=27.5, length=1.0), **PRESET_DEFAULTS
    )
    mydhl_express_pak = lib.units.PackagePreset(
        **dict(width=40.0, height=30.0, length=2.0), **PRESET_DEFAULTS
    )
    mydhl_small_parcel = lib.units.PackagePreset(
        **dict(width=30.0, height=20.0, length=10.0), **PRESET_DEFAULTS
    )
    mydhl_medium_parcel = lib.units.PackagePreset(
        **dict(width=50.0, height=40.0, length=20.0), **PRESET_DEFAULTS
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
    """MyDHL specific weight unit"""
    KG = "kg"
    G = "g"


class DimensionUnit(lib.StrEnum):
    """MyDHL specific dimension unit"""
    CM = "cm"
    MM = "mm"


class PackagingType(lib.StrEnum):
    """MyDHL specific packaging type"""
    ENVELOPE = "envelope"
    PAK = "pak"
    PARCEL = "parcel"
    BOX = "box"

    """ Unified Packaging type mapping """
    envelope = ENVELOPE
    pak = PAK
    tube = PARCEL
    pallet = PARCEL
    small_box = BOX
    medium_box = BOX
    your_packaging = PARCEL


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", LabelType)


class ShippingService(lib.StrEnum):
    """MyDHL shipping services"""
    mydhl_express_9_00 = "Express 9:00"
    mydhl_express_10_30 = "Express 10:30"
    mydhl_express_12_00 = "Express 12:00"
    mydhl_express_worldwide = "Express Worldwide"
    mydhl_express_worldwide_doc = "Express Worldwide Documents"
    mydhl_express_break_bulk_express = "Break Bulk Express"
    mydhl_express_break_bulk_economy = "Break Bulk Economy"
    mydhl_express_medical_express = "Medical Express"
    mydhl_express_europack = "Europack"


class ShippingOption(lib.Enum):
    """MyDHL specific shipping options."""
    
    mydhl_insurance = lib.OptionEnum("insurance", float)
    mydhl_declared_value = lib.OptionEnum("declared_value", float)
    mydhl_paperless_trade = lib.OptionEnum("paperless_trade", bool)
    mydhl_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    mydhl_dangerous_goods = lib.OptionEnum("dangerous_goods", bool)
    mydhl_pickup_time = lib.OptionEnum("pickup_time", str)
    mydhl_special_services = lib.OptionEnum("special_services", list)
    mydhl_customs_declaration = lib.OptionEnum("customs_declaration", dict)
    mydhl_delivery_notification = lib.OptionEnum("delivery_notification", bool)
    mydhl_signature_required = lib.OptionEnum("signature_required", bool)

    """Unified Option type mapping"""
    insurance = mydhl_insurance
    declared_value = mydhl_declared_value
    saturday_delivery = mydhl_saturday_delivery
    signature_confirmation = mydhl_signature_required


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
    on_hold = ["ON_HOLD", "CUSTOMS_DELAY"]
    delivered = ["DELIVERED", "FINAL_DELIVERY"]
    in_transit = ["IN_TRANSIT", "FORWARDED", "CUSTOMS_CLEARANCE", "PROCESSED"]
    delivery_failed = ["DELIVERY_FAILED", "DAMAGED", "LOST"]
    delivery_delayed = ["DELAYED", "EXCEPTION"]
    out_for_delivery = ["OUT_FOR_DELIVERY", "WITH_DELIVERY_COURIER"]
    ready_for_pickup = ["READY_FOR_PICKUP", "DEPOT_PICKUP"]


# Legacy aliases for backward compatibility
MyDHLService = ShippingService
MyDHLOption = ShippingOption
ServiceType = ShippingService
