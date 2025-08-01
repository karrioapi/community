import karrio.lib as lib


class LabelFormat(lib.Enum):
    PDF = "PDF"


class WeightUnit(lib.Enum):
    KG = "KG"
    LB = "LB"


class DimensionUnit(lib.Enum):
    CM = "CM"
    IN = "IN"


class PackagePresets(lib.Enum):
    gls_eu_envelope = lib.units.PackagePreset(
        width=35.0, height=27.5, length=1.0, weight_unit="KG", dimension_unit="CM"
    )


class ServiceType(lib.Enum):
    gls_eu_business_parcel = "BP"
    gls_eu_express = "EXP"
    gls_eu_flex_delivery_service = "FDS"


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingOption(lib.Enum):
    gls_eu_cash_on_delivery = lib.OptionEnum("cash_on_delivery", float)
    gls_eu_insurance = lib.OptionEnum("insurance", float)
    gls_eu_delivery_notification = lib.OptionEnum("delivery_notification", bool)
    gls_eu_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
