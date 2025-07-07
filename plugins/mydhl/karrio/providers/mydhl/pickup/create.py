"""Karrio MyDHL pickup create API implementation."""

import karrio.schemas.mydhl.pickup_create_request as mydhl_req
import karrio.schemas.mydhl.pickup_create_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    pickup = _extract_details(response, settings) if response and not messages else None

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from MyDHL response."""
    # For simple JSON responses, extract directly
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=data.get("confirmationNumber", ""),
        pickup_date=lib.fdate(data.get("pickupDate")),
        ready_time=data.get("readyTime"),
        closing_time=data.get("closingTime"),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create MyDHL pickup request."""
    address = lib.to_address(payload.address)

    request = mydhl_req.PickupCreateRequestType(
        plannedPickupDateAndTime=lib.fdatetime(
            payload.pickup_date,
            current_format="%Y-%m-%d",
            output_format="%Y-%m-%dT%H:%M:%S GMT+01:00"
        ),
        closeTime=payload.closing_time or "18:00",
        location="reception",
        accounts=[
            mydhl_req.AccountType(
                typeCode="shipper",
                number=settings.account_number,
            )
        ],
        customerDetails=mydhl_req.CustomerDetailsType(
            shipperDetails=mydhl_req.DetailsType(
                postalAddress=mydhl_req.PostalAddressType(
                    cityName=address.city,
                    countryCode=address.country_code,
                    postalCode=address.postal_code,
                    addressLine1=address.address_line1,
                ),
                contactInformation=mydhl_req.ContactInformationType(
                    companyName=address.company_name,
                    fullName=address.person_name,
                    phone=address.phone_number,
                    email=address.email,
                ),
            ),
        ),
        shipmentDetails=[
            mydhl_req.ShipmentDetailType(
                productCode="U",
                packages=[
                    mydhl_req.PackageType(
                        weight=1.0,
                        dimensions=mydhl_req.DimensionsType(
                            length=1,
                            width=1,
                            height=1,
                        ),
                    )
                ],
            )
        ],
    )

    return lib.Serializable(request, lib.to_dict)