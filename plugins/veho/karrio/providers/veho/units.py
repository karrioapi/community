import karrio.lib as lib
import karrio.core.units as units

PRESET_DEFAULTS = dict(
    dimension_unit="IN",
    weight_unit="LB",
)

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_lb=0.01,
    min_in=0.01,
)


class PackagePresets(lib.Enum):
    """
    Note that dimensions are in IN and weight in LB
    """
    veho_small_package = lib.units.PackagePreset(
        **dict(width=8.0, height=6.0, length=4.0), **PRESET_DEFAULTS
    )
    veho_medium_package = lib.units.PackagePreset(
        **dict(width=12.0, height=9.0, length=6.0), **PRESET_DEFAULTS
    )
    veho_large_package = lib.units.PackagePreset(
        **dict(width=18.0, height=12.0, length=8.0), **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
    PDF_4x6 = ("PDF", "4x6")
    PNG_4x6 = ("PNG", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    PNG = PNG_4x6


class PackagingType(lib.StrEnum):
    """Veho specific packaging type"""
    PACKAGE = "PACKAGE"
    BOX = "PACKAGE"  # Map BOX to PACKAGE for Veho API

    """Unified Packaging type mapping"""
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class PaymentType(lib.StrEnum):
    account = "Account"
    sender = account
    recipient = account
    third_party = account


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    label_type = lib.OptionEnum("label_type", LabelType)


class ShippingService(lib.StrEnum):
    """Veho specific services based on OpenAPI spec"""
    veho_next_day = "nextDay"
    veho_same_day = "sameDay"
    veho_two_day = "twoDay"
    veho_value = "vehoValue"
    veho_ground_plus = "groundPlus"
    veho_premium_economy = "premiumEconomy"
    veho_express_air = "expressAir"


class ShippingOption(lib.Enum):
    """Veho specific shipping options."""
    
    veho_delivery_max_datetime = lib.OptionEnum("delivery_max_datetime", str)
    veho_label_date = lib.OptionEnum("label_date", str)
    veho_insurance = lib.OptionEnum("insurance", float)
    veho_signature_required = lib.OptionEnum("signature_required", bool)
    veho_delivery_confirmation = lib.OptionEnum("delivery_confirmation", bool)

    """Unified Option type mapping"""
    insurance = veho_insurance
    signature_confirmation = veho_signature_required
    delivery_confirmation = veho_delivery_confirmation


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
    on_hold = ["ON_HOLD", "EXCEPTION"]
    delivered = ["DELIVERED", "FINAL_DELIVERY"]
    in_transit = ["IN_TRANSIT", "PROCESSED", "SHIPMENT_INFORMATION_RECEIVED"]
    delivery_failed = ["DELIVERY_FAILED", "RETURNED_TO_SENDER"]
    out_for_delivery = ["OUT_FOR_DELIVERY", "WITH_DELIVERY_COURIER"]
    delivery_delayed = ["DELIVERY_DELAYED"]
    pickup_failed = ["PICKUP_FAILED"]


def is_ground_plus(service: str) -> bool:
    """Check if the service is Veho Ground Plus"""
    return service == ShippingService.veho_ground_plus


def is_premium_economy(service: str) -> bool:
    """Check if the service is Veho Premium Economy"""
    return service == ShippingService.veho_premium_economy


def get_service_name(service: str) -> str:
    """Get the display name for a service"""
    service_names = {
        ShippingService.veho_next_day: "Veho Next Day",
        ShippingService.veho_same_day: "Veho Same Day",
        ShippingService.veho_two_day: "Veho Two Day",
        ShippingService.veho_value: "Veho Value",
        ShippingService.veho_ground_plus: "Veho Ground Plus",
        ShippingService.veho_premium_economy: "Veho Premium Economy",
        ShippingService.veho_express_air: "Veho Express Air",
    }
    return service_names.get(service, service)


# Legacy aliases for backward compatibility
VehoService = ShippingService
VehoOption = ShippingOption
