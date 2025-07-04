"""Karrio ShipEngine units."""

import karrio.lib as lib

# ShipEngine is a hub carrier supporting multiple services
ShippingService = lib.units.create_enum(
    "ShippingService",
    {
        # UPS Services
        "ups_ground": "UPS Ground",
        "ups_2_day_air": "UPS 2nd Day Air",
        "ups_next_day_air": "UPS Next Day Air",
        "ups_express": "UPS Express",
        "ups_worldwide_express": "UPS Worldwide Express",
        "ups_worldwide_express_plus": "UPS Worldwide Express Plus",
        "ups_3_day_select": "UPS 3 Day Select",
        "ups_express_saver": "UPS Express Saver",
        
        # FedEx Services
        "fedex_ground": "FedEx Ground",
        "fedex_2_day": "FedEx 2 Day",
        "fedex_express_overnight": "FedEx Express Overnight",
        "fedex_standard_overnight": "FedEx Standard Overnight",
        "fedex_priority_overnight": "FedEx Priority Overnight",
        "fedex_international_economy": "FedEx International Economy",
        "fedex_international_priority": "FedEx International Priority",
        "fedex_international_first": "FedEx International First",
        "fedex_express_saver": "FedEx Express Saver",
        
        # USPS Services
        "usps_priority_mail": "USPS Priority Mail",
        "usps_priority_mail_express": "USPS Priority Mail Express",
        "usps_first_class_mail": "USPS First Class Mail",
        "usps_media_mail": "USPS Media Mail",
        "usps_parcel_select": "USPS Parcel Select",
        "usps_priority_mail_international": "USPS Priority Mail International",
        "usps_priority_mail_express_international": "USPS Priority Mail Express International",
        "usps_first_class_mail_international": "USPS First Class Mail International",
        
        # DHL Services
        "dhl_express": "DHL Express",
        "dhl_express_12": "DHL Express 12",
        "dhl_express_10_30": "DHL Express 10:30",
        "dhl_express_worldwide": "DHL Express Worldwide",
        "dhl_economy_select": "DHL Economy Select",
        
        # Canada Post Services
        "canada_post_regular_parcel": "Canada Post Regular Parcel",
        "canada_post_expedited_parcel": "Canada Post Expedited Parcel",
        "canada_post_xpresspost": "Canada Post Xpresspost",
        "canada_post_priority": "Canada Post Priority",
        
        # OnTrac Services
        "ontrac_ground": "OnTrac Ground",
        "ontrac_sunrise": "OnTrac Sunrise",
        "ontrac_gold": "OnTrac Gold",
        
        # LSO Services
        "lso_ground": "LSO Ground",
        "lso_2_day": "LSO 2 Day",
        "lso_next_day": "LSO Next Day",
        
        # Stamps.com Services
        "stamps_com_priority_mail": "Stamps.com Priority Mail",
        "stamps_com_first_class_mail": "Stamps.com First Class Mail",
        "stamps_com_media_mail": "Stamps.com Media Mail",
        
        # Generic Services
        "standard": "Standard",
        "express": "Express",
        "overnight": "Overnight",
        "ground": "Ground",
        "international": "International",
        "priority": "Priority",
        "economy": "Economy",
        "expedited": "Expedited",
        "next_day": "Next Day",
        "2_day": "2 Day",
        "3_day": "3 Day",
    },
)


class ShippingOption(lib.Enum):
    # ShipEngine specific options
    shipengine_carrier_id = lib.OptionEnum("shipengine_carrier_id")
    shipengine_service_code = lib.OptionEnum("shipengine_service_code")
    shipengine_package_code = lib.OptionEnum("shipengine_package_code")
    shipengine_confirmation_type = lib.OptionEnum("shipengine_confirmation_type")
    shipengine_label_format = lib.OptionEnum("shipengine_label_format")
    shipengine_label_layout = lib.OptionEnum("shipengine_label_layout")
    shipengine_display_scheme = lib.OptionEnum("shipengine_display_scheme")
    shipengine_dry_ice = lib.OptionEnum("shipengine_dry_ice", bool)
    shipengine_dry_ice_weight = lib.OptionEnum("shipengine_dry_ice_weight")
    shipengine_saturday_delivery = lib.OptionEnum("shipengine_saturday_delivery", bool)
    shipengine_non_machinable = lib.OptionEnum("shipengine_non_machinable", bool)
    shipengine_contains_alcohol = lib.OptionEnum("shipengine_contains_alcohol", bool)
    shipengine_delivered_duty_paid = lib.OptionEnum("shipengine_delivered_duty_paid", bool)
    shipengine_bill_to_account = lib.OptionEnum("shipengine_bill_to_account")
    shipengine_bill_to_country_code = lib.OptionEnum("shipengine_bill_to_country_code")
    shipengine_bill_to_party = lib.OptionEnum("shipengine_bill_to_party")
    shipengine_bill_to_postal_code = lib.OptionEnum("shipengine_bill_to_postal_code")
    shipengine_freight_class = lib.OptionEnum("shipengine_freight_class")
    shipengine_freight_charge = lib.OptionEnum("shipengine_freight_charge")
    shipengine_cod_payment_type = lib.OptionEnum("shipengine_cod_payment_type")
    shipengine_cod_payment_amount = lib.OptionEnum("shipengine_cod_payment_amount")
    shipengine_validate_address = lib.OptionEnum("shipengine_validate_address")
    shipengine_rate_id = lib.OptionEnum("shipengine_rate_id")
    shipengine_warehouse_id = lib.OptionEnum("shipengine_warehouse_id")
    shipengine_reference1 = lib.OptionEnum("shipengine_reference1")
    shipengine_reference2 = lib.OptionEnum("shipengine_reference2")
    shipengine_reference3 = lib.OptionEnum("shipengine_reference3")
    
    # Generic unified options
    saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    signature_confirmation = lib.OptionEnum("signature_confirmation", bool)
    adult_signature = lib.OptionEnum("adult_signature", bool)
    insurance = lib.OptionEnum("insurance", float)
    dry_ice = lib.OptionEnum("dry_ice", bool)
    dangerous_goods = lib.OptionEnum("dangerous_goods", bool)
    hold_at_location = lib.OptionEnum("hold_at_location", bool)
    cod = lib.OptionEnum("cod", float)
    residential = lib.OptionEnum("residential", bool)
    notification = lib.OptionEnum("notification", bool)
    collect_on_delivery = lib.OptionEnum("collect_on_delivery", bool)
    bill_to_third_party = lib.OptionEnum("bill_to_third_party", bool)
    delivery_confirmation = lib.OptionEnum("delivery_confirmation", bool)
    hazmat = lib.OptionEnum("hazmat", bool)
    oversize = lib.OptionEnum("oversize", bool)
    freight = lib.OptionEnum("freight", bool)
    consolidate = lib.OptionEnum("consolidate", bool)
    insured_value = lib.OptionEnum("insured_value", float)
    return_receipt = lib.OptionEnum("return_receipt", bool)
    restricted_delivery = lib.OptionEnum("restricted_delivery", bool)
    declared_value = lib.OptionEnum("declared_value", float)
    reference_number = lib.OptionEnum("reference_number")
    pickup_date = lib.OptionEnum("pickup_date")
    delivery_date = lib.OptionEnum("delivery_date")
    special_instructions = lib.OptionEnum("special_instructions")


class TrackingStatus(lib.Enum):
    unknown = "UN"
    not_yet_in_system = "NY"
    in_transit = "IT"
    delivered = "DE"
    exception = "EX"
    accepted = "AC"
    at_pickup = "AT"
    at_location = "AT_LOCATION"
    information_received = "INFORMATION_RECEIVED"
    out_for_delivery = "OUT_FOR_DELIVERY"
    picked_up = "PICKED_UP"


# Unified mapping for units initialization
def shipping_options_initializer(options: dict, package_options: dict = None) -> dict:
    """
    ShipEngine shipping options initialization
    """
    options = options or {}
    if package_options is not None:
        options.update(package_options)
    return options 
