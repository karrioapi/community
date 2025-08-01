import karrio.lib as lib


class PackagePresets(lib.Enum):
    mydhl_express_envelope = lib.units.PackagePreset(
        width=35.0, height=27.5, length=1.0, weight_unit="KG", dimension_unit="CM"
    )
    mydhl_express_pak = lib.units.PackagePreset(
        width=40.0, height=30.0, length=2.0, weight_unit="KG", dimension_unit="CM"
    )


class ServiceType(lib.Enum):
    mydhl_express_9_00 = "9:00"
    mydhl_express_10_30 = "10:30"
    mydhl_express_12_00 = "12:00"
    mydhl_express_worldwide = "W"
    mydhl_express_worldwide_doc = "U"
    mydhl_express_break_bulk_express = "H"
    mydhl_express_break_bulk_economy = "E"
    mydhl_express_medical_express = "M"
    mydhl_express_europack = "V"


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class ShippingOption(lib.Enum):
    mydhl_insurance = lib.OptionEnum("insurance", float)
    mydhl_declared_value = lib.OptionEnum("declared_value", float)
    mydhl_paperless_trade = lib.OptionEnum("paperless_trade", bool)
    mydhl_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    mydhl_dangerous_goods = lib.OptionEnum("dangerous_goods", bool)
