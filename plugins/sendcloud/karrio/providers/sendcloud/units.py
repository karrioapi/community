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
    sendcloud_small_parcel = lib.units.PackagePreset(
        **dict(width=20.0, height=15.0, length=10.0), **PRESET_DEFAULTS
    )
    sendcloud_medium_parcel = lib.units.PackagePreset(
        **dict(width=30.0, height=20.0, length=15.0), **PRESET_DEFAULTS
    )
    sendcloud_large_parcel = lib.units.PackagePreset(
        **dict(width=50.0, height=40.0, length=30.0), **PRESET_DEFAULTS
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
    account = "Account"
    sender = account
    recipient = account
    third_party = account


class PackagingType(lib.StrEnum):
    """Sendcloud specific packaging type"""
    PACKAGE = "parcel"
    ENVELOPE = "envelope"
    LETTER = "letter"

    """ Unified Packaging type mapping """
    envelope = ENVELOPE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class WeightUnit(lib.StrEnum):
    """Sendcloud specific weight unit"""
    KG = "kg"
    G = "g"


class DimensionUnit(lib.StrEnum):
    """Sendcloud specific dimension unit"""
    CM = "cm"
    MM = "mm"


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", LabelType)


class ShippingService(lib.StrEnum):
    """Sendcloud shipping services"""
    sendcloud_standard = "Standard"
    sendcloud_express = "Express"
    sendcloud_one_day = "One Day"
    sendcloud_same_day = "Same Day"


class ShippingOption(lib.Enum):
    """Sendcloud specific shipping options."""
    
    sendcloud_service_point_id = lib.OptionEnum("service_point_id", str)
    sendcloud_insured_value = lib.OptionEnum("insured_value", float)
    sendcloud_contents = lib.OptionEnum("contents", str)
    sendcloud_require_signature = lib.OptionEnum("require_signature", bool)
    sendcloud_reference = lib.OptionEnum("reference", str)
    sendcloud_customs_invoice_nr = lib.OptionEnum("customs_invoice_nr", str)
    sendcloud_customs_shipment_type = lib.OptionEnum("customs_shipment_type", str)
    sendcloud_order_number = lib.OptionEnum("order_number", str)
    sendcloud_sender_address_id = lib.OptionEnum("sender_address_id", str)
    sendcloud_brand_id = lib.OptionEnum("brand_id", str)

    """Unified Option type mapping"""
    insurance = sendcloud_insured_value
    signature_confirmation = sendcloud_require_signature


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
    on_hold = ["ANNOUNCED", "ON_HOLD"]
    delivered = ["DELIVERED", "FINAL_DELIVERY"]
    in_transit = ["IN_TRANSIT", "READY_TO_BE_SHIPPED", "BEING_SORTED", "PROCESSED"]
    delivery_failed = ["DELIVERY_FAILED", "UNABLE_TO_DELIVER", "NO_SHOW"]
    delivery_delayed = ["DELIVERY_DELAYED"]
    out_for_delivery = ["OUT_FOR_DELIVERY", "WITH_DELIVERY_COURIER"]
    ready_for_pickup = ["READY_TO_BE_COLLECTED", "PICKUP_READY"]


# Legacy aliases for backward compatibility
SendcloudService = ShippingService
SendcloudOption = ShippingOption
LabelFormat = LabelType
