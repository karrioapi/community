""" Aramex Native Types """

import karrio.lib as lib


class TrackingIncidentReason(lib.Enum):
    """Maps Aramex exception codes to normalized TrackingIncidentReason."""
    carrier_damaged_parcel = ["DMG", "DAMAGE", "DAMAGED"]
    carrier_sorting_error = ["MISROUTE"]
    carrier_parcel_lost = ["LOST"]
    carrier_vehicle_issue = ["DELAY", "VEHICLE"]

    consignee_refused = ["REFUSED", "REF", "REJECT"]
    consignee_business_closed = ["CLOSED", "BUSINESS_CLOSED"]
    consignee_not_home = ["NOTHOME", "NH", "NOT_HOME"]
    consignee_incorrect_address = ["BADADDR", "INCORRECT", "WRONG_ADDRESS"]
    consignee_access_restricted = ["NOACCESS", "RESTRICTED"]

    customs_delay = ["CUSTOMS", "CUSTOMSHOLD", "CUSTOMS_DELAY"]
    customs_documentation = ["CUSTOMSDOC", "CUSTOMS_DOCUMENTS"]
    customs_duties_unpaid = ["CUSTOMS_UNPAID", "DUTIES"]

    weather_delay = ["WEATHER"]

    delivery_exception_hold = ["HOLD", "ONHOLD", "HELD"]
    delivery_exception_undeliverable = ["UNDELIVERABLE", "UNABLE"]

    unknown = []


# import karrio.lib as lib
# from karrio.core.utils import Enum, Flag
#
# PRESET_DEFAULTS = dict(dimension_unit="CM", weight_unit="KG")
#
#
# class PackagePresets(lib.Enum):
#     # carrier_envelope = PackagePreset(
#     #     **dict(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="envelope"),
#     #     **PRESET_DEFAULTS
#     # )
#     # carrier_box = PackagePreset(
#     #     **dict(weight=0.5, width=35.0, height=27.5, length=1.0, packaging_type="medium_box"),
#     #     **PRESET_DEFAULTS
#     # )
#     pass


# class PackageType(lib.StrEnum):
#     carrier_envelope = "ENVELOPE CODE"
#     carrier_box = "BOX CODE"
#     carrier_your_packaging = "CUSTOM PACKAGING CODE"
#
#     """ Unified Packaging type mapping """
#     envelope = carrier_envelope
#     pak = carrier_envelope
#     tube = carrier_your_packaging
#     pallet = carrier_your_packaging
#     small_box = carrier_box
#     medium_box = carrier_box
#     large_box = carrier_box
#     your_packaging = carrier_your_packaging
#
#
# class Service(Enum):
#     carrier_standard = "STANDARD CODE"
#     carrier_premium = "PREMIUM CODE"
#     carrier_overnight = "OVERNIGHT CODE"
#
#
# class Option(lib.Enum):
#     carrier_signature = "SIGNATURE CODE"
#     carrier_saturday_delivery = "SATURDAY DELIVERY CODE"
#     carrier_dry_ice = "DRY ICE CODE"
#
