"""Karrio ShipEngine shipment creation implementation."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.shipengine.error as error
import karrio.providers.shipengine.utils as provider_utils
import karrio.providers.shipengine.units as provider_units
import karrio.schemas.shipengine.shipment_request as shipengine_req
import karrio.schemas.shipengine.shipment_response as shipengine_res


def parse_shipment_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = lib.to_object(shipengine_res.ShipmentResponseType, response)
    
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.tracking_number or "",
        shipment_identifier=shipment.label_id or "",
        docs=models.Documents(
            label=lib.failsafe(lambda: shipment.label_download.pdf) or ""
        ),
        meta=dict(
            carrier_code=shipment.carrier_code,
            service_code=shipment.service_code,
            label_format="PDF",
            shipment_id=shipment.shipment_id,
            carrier_id=shipment.carrier_id,
            tracking_url=f"https://www.shipengine.com/tracking/{shipment.tracking_number or ''}",
        ),
    ), messages


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    service_identifier = lib.identity(
        service.value_or_key if service else payload.service or ""
    )
    service_code, carrier_id = _parse_service_selection(service_identifier, settings)

    request = shipengine_req.ShipmentRequestType(
        shipment=shipengine_req.ShipmentType(
            service_code=service_code,
            ship_to=shipengine_req.ShipType(
                name=recipient.person_name,
                phone=recipient.phone_number,
                company_name=recipient.company_name,
                address_line1=recipient.address_line1,
                address_line2=recipient.address_line2,
                city_locality=recipient.city,
                state_province=recipient.state_code,
                postal_code=lib.failsafe(lambda: int(recipient.postal_code)) if recipient.postal_code and recipient.postal_code.isdigit() else None,
                country_code=recipient.country_code,
                address_residential_indicator="yes" if recipient.residential else "no",
            ),
            ship_from=shipengine_req.ShipType(
                name=shipper.person_name,
                phone=shipper.phone_number,
                company_name=shipper.company_name,
                address_line1=shipper.address_line1,
                address_line2=shipper.address_line2,
                city_locality=shipper.city,
                state_province=shipper.state_code,
                postal_code=lib.failsafe(lambda: int(shipper.postal_code)) if shipper.postal_code and shipper.postal_code.isdigit() else None,
                country_code=shipper.country_code,
                address_residential_indicator="yes" if shipper.residential else "no",
            ),
            packages=[
                shipengine_req.PackageType(
                    weight=shipengine_req.WeightType(
                        value=package.weight.value,
                        unit=lib.failsafe(lambda: provider_units.WeightUnit[package.weight.unit].value, "pound"),
                    ),
                    dimensions=lib.identity(
                        shipengine_req.DimensionsType(
                            unit=lib.failsafe(lambda: provider_units.DimensionUnit[package.dimension_unit or "IN"].value, "inch"),
                            length=package.length.value,
                            width=package.width.value,
                            height=package.height.value,
                        ) if all([package.length, package.width, package.height]) else None
                    ),
                )
                for package in packages
            ],
        ),
        label_format="pdf",
        label_layout="4x6",
    )

    # Add carrier_id manually since it's not in the schema
    request_dict = lib.to_dict(request)
    lib.identity(
        request_dict["shipment"].update({"carrier_id": carrier_id})
        if carrier_id else None
    )

    return lib.Serializable(request_dict, lib.to_dict)


def _parse_service_selection(service_identifier: str, settings: provider_utils.Settings) -> typing.Tuple[str, str]:
    """Parse service selection to extract service code and carrier ID."""
    # If it's a rate_id from previous rate request, use it directly
    if service_identifier.startswith("se-"):
        return service_identifier, ""

    # Extract service code from dynamic service identifier
    if service_identifier.startswith("shipengine_"):
        parts = service_identifier.split("_", 2)
        if len(parts) >= 3:
            carrier_code = parts[1]
            service_code = "_".join(parts[2:])

            # Look up carrier_id from settings or use carrier_code
            carrier_id = _get_carrier_id(carrier_code, settings)
            return service_code, carrier_id

    # Default to service code
    return service_identifier, ""


def _get_carrier_id(carrier_code: str, settings: provider_utils.Settings) -> str:
    """Get ShipEngine carrier ID for a carrier code."""
    # This would typically come from configuration or a carrier lookup
    # For now, return empty string to let ShipEngine auto-select
    return ""

