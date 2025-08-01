import enum
import karrio.lib as lib

class ConnectionConfig(lib.Enum):
    """DHL eCommerce Americas connection configuration options"""
    shipping_services = lib.OptionEnum("shipping_services")


class ConnectionConfig(lib.Enum):
    """DHL eCommerce Americas connection configuration options"""
    shipping_services = lib.OptionEnum("shipping_services")


class DHLService(lib.StrEnum):
    """DHL eCommerce Americas service codes."""
    
    dhl_parcel_ground = "DHLParcelGround"
    dhl_parcel_expedited = "DHLParcelExpedited"
    dhl_parcel_expedited_max = "DHLParcelExpeditedMax"
    dhl_bpm_expedited = "DHLBPMExpedited"
    dhl_bpm_ground = "DHLBPMGround"
    dhl_marketing_parcel_ground = "DHLMarketingParcelGround"
    dhl_marketing_parcel_expedited = "DHLMarketingParcelExpedited"
    
    dhl_parcel_international_direct = "DHLParcelInternationalDirect"
    dhl_parcel_international_standard = "DHLParcelInternationalStandard"
    dhl_packet_international = "DHLPacketInternational"
    dhl_packet_plus_international = "DHLPacketPlusInternational"
    dhl_packet_ipa = "DHLPacketIPA"
    dhl_parcel_international_direct_priority = "DHLParcelInternationalDirectPriority"
    dhl_parcel_international_direct_standard = "DHLParcelInternationalDirectStandard"
    dhl_parcel_international_direct_smb = "DHLParcelInternationalDirectSMB"
    dhl_parcel_international_standard_smb = "DHLParcelInternationalStandardSMB"
    
    dhl_smart_mail_parcel_return_ground = "DHLSmartMailParcelReturnGround"
    dhl_smart_mail_parcel_return_plus = "DHLSmartMailParcelReturnPlus"
    dhl_smart_mail_parcel_return_light = "DHLSmartMailParcelReturnLight"


class DHLOption(lib.StrEnum):
    """DHL eCommerce Americas shipping options."""
    
    signature_required = "SignatureRequired"
    adult_signature = "AdultSignature"
    delivery_confirmation = "DeliveryConfirmation"
    insurance = "Insurance"
    saturday_delivery = "SaturdayDelivery"
    delivery_duty_paid = "DDP"
    delivery_duty_unpaid = "DDU"
    print_custom_1 = "print_custom_1"


ShippingService = DHLService
ShippingOption = DHLOption


def shipping_options_initializer(
    options: dict,
    package_options: dict = None,
) -> dict:
    """Initialize shipping options for DHL eCommerce Americas."""
    
    _options = options.copy()
    
    if package_options is not None:
        _options.update(package_options)

    return _options


TrackingStatus = lib.units.TrackingStatus
PackagingUnit = lib.units.PackagingUnit
WeightUnit = lib.units.WeightUnit
DimensionUnit = lib.units.DimensionUnit
