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
    dhl_small_box = lib.units.PackagePreset(
        **dict(width=8.0, height=6.0, length=4.0), **PRESET_DEFAULTS
    )
    dhl_medium_box = lib.units.PackagePreset(
        **dict(width=12.0, height=9.0, length=6.0), **PRESET_DEFAULTS
    )
    dhl_large_box = lib.units.PackagePreset(
        **dict(width=18.0, height=12.0, length=8.0), **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
    PNG_4x6 = ("PNG", "4x6")
    PNG_4x8 = ("PNG", "4x8")
    PDF_4x6 = ("PDF", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    PNG = PNG_4x6


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
    """DHL eCommerce Americas service codes."""
    
    dhl_parcel_ground = "DHLParcelGround"
    dhl_parcel_expedited = "DHLParcelExpedited"
    dhl_parcel_expedited_max = "DHLParcelExpeditedMax"
    dhl_bpm_expedited = "DHLBPMExpedited"
    dhl_bpm_ground = "DHLBPMGround"
    dhl_marketing_parcel_ground = "DHLMarketingParcelGround"
    dhl_marketing_parcel_expedited = "DHLMarketingParcelExpedited"
    
    # International services
    dhl_parcel_international_direct = "DHLParcelInternationalDirect"
    dhl_parcel_international_standard = "DHLParcelInternationalStandard"
    dhl_packet_international = "DHLPacketInternational"
    dhl_packet_plus_international = "DHLPacketPlusInternational"
    dhl_packet_ipa = "DHLPacketIPA"
    dhl_parcel_international_direct_priority = "DHLParcelInternationalDirectPriority"
    dhl_parcel_international_direct_standard = "DHLParcelInternationalDirectStandard"
    dhl_parcel_international_direct_smb = "DHLParcelInternationalDirectSMB"
    dhl_parcel_international_standard_smb = "DHLParcelInternationalStandardSMB"
    
    # Return services
    dhl_smart_mail_parcel_return_ground = "DHLSmartMailParcelReturnGround"
    dhl_smart_mail_parcel_return_plus = "DHLSmartMailParcelReturnPlus"
    dhl_smart_mail_parcel_return_light = "DHLSmartMailParcelReturnLight"


class ShippingOption(lib.Enum):
    """DHL eCommerce Americas shipping options."""
    
    dhl_signature_required = lib.OptionEnum("signature_required", bool)
    dhl_adult_signature = lib.OptionEnum("adult_signature", bool)
    dhl_delivery_confirmation = lib.OptionEnum("delivery_confirmation", bool)
    dhl_insurance = lib.OptionEnum("insurance", float)
    dhl_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    dhl_delivery_duty_paid = lib.OptionEnum("delivery_duty_paid", bool)
    dhl_delivery_duty_unpaid = lib.OptionEnum("delivery_duty_unpaid", bool)

    """Unified Option type mapping"""
    insurance = dhl_insurance
    signature_confirmation = dhl_signature_required
    saturday_delivery = dhl_saturday_delivery


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
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


# Legacy aliases for backward compatibility
DHLService = ShippingService
DHLOption = ShippingOption