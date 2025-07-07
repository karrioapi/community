import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """MyDHL packaging types."""
    dhl_express_envelope = "EE"
    dhl_express_easy = "OD"
    dhl_express_box = "YP"
    dhl_express_tube = "DF"
    dhl_jumbo_box = "JJ"
    dhl_jumbo_box_plus = "JP"
    customer_packaging = "CP"

    """Unified Packaging type mapping."""
    envelope = dhl_express_envelope
    pak = dhl_express_easy
    small_box = dhl_express_box
    medium_box = dhl_express_box
    large_box = dhl_jumbo_box
    tube = dhl_express_tube
    your_packaging = customer_packaging


class PackagePresets(lib.Enum):
    """MyDHL package presets."""
    mydhl_box_2 = lib.units.PackagePreset(
        **dict(width=25, height=15, length=30, weight_unit="KG", dimension_unit="CM")
    )
    mydhl_box_5 = lib.units.PackagePreset(
        **dict(width=30, height=20, length=35, weight_unit="KG", dimension_unit="CM")
    )
    mydhl_box_10 = lib.units.PackagePreset(
        **dict(width=35, height=25, length=40, weight_unit="KG", dimension_unit="CM")
    )


class ShippingService(lib.StrEnum):
    """MyDHL service types."""
    dhl_express_worldwide = "U"      # Express Worldwide
    dhl_express_12_00 = "T"          # Express 12:00
    dhl_express_10_30 = "K"          # Express 10:30
    dhl_express_09_00 = "Y"          # Express 9:00
    dhl_express_envelope = "D"        # Express Envelope
    dhl_economy_select = "W"          # Economy Select
    dhl_break_bulk_express = "B"      # Break Bulk Express
    dhl_medical_express = "M"         # Medical Express


class ShippingOption(lib.Enum):
    """MyDHL shipping options."""
    dhl_insurance = lib.OptionEnum("II", float)
    dhl_signature_required = lib.OptionEnum("PW", bool)
    dhl_saturday_delivery = lib.OptionEnum("AA", bool)
    dhl_cash_on_delivery = lib.OptionEnum("CD", float)
    dhl_dangerous_goods = lib.OptionEnum("HH", bool)
    dhl_electronic_trade_documents = lib.OptionEnum("WY", bool)

    """Unified Option type mapping."""
    insurance = dhl_insurance
    signature_required = dhl_signature_required
    saturday_delivery = dhl_saturday_delivery
    cash_on_delivery = dhl_cash_on_delivery


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to shipping options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """MyDHL tracking status mapping."""
    on_hold = ["OH", "AD"]
    delivered = ["OK", "DD"]
    in_transit = ["PU", "CC", "AR", "AF", "PL", "DF", "UD", "MC"]
    delivery_failed = ["RT", "MS", "HI", "UD", "HO"]
    out_for_delivery = ["WC", "OD"]
    ready_for_pickup = ["RD"]


class WeightUnit(lib.Enum):
    """MyDHL weight units."""
    KG = "KG"
    LB = "LB"


class DimensionUnit(lib.Enum):
    """MyDHL dimension units."""
    CM = "CM"
    IN = "IN"