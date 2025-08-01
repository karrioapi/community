import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.gls_eu.shipment.create as shipment
import karrio.providers.gls_eu.shipment.cancel as shipment_cancel
import karrio.providers.gls_eu.tracking as tracking
import karrio.providers.gls_eu.pickup.create as pickup
import karrio.mappers.gls_eu.settings as provider_settings


class Mapper(
    lib.Mapper,
    lib.PickupMapper,
    lib.ShipmentMapper,
    lib.TrackingMapper,
):
    settings: provider_settings.Settings

    def create_tracking_request(
        self, payload: models.TrackingRequest
    ) -> lib.Serializable:
        return tracking.tracking_request(payload, self.settings)

    def parse_tracking_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
        return tracking.parse_tracking_response(response, self.settings)

    def create_shipment_request(
        self, payload: models.ShipmentRequest
    ) -> lib.Serializable:
        return shipment.shipment_request(payload, self.settings)

    def parse_shipment_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
        return shipment.parse_shipment_response(response, self.settings)

    def create_shipment_cancel_request(
        self, payload: models.ShipmentCancelRequest
    ) -> lib.Serializable:
        return shipment_cancel.shipment_cancel_request(payload, self.settings)

    def parse_shipment_cancel_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
        return shipment_cancel.parse_shipment_cancel_response(response, self.settings)

    def create_pickup_request(
        self, payload: models.PickupRequest
    ) -> lib.Serializable:
        return pickup.pickup_request(payload, self.settings)

    def parse_pickup_response(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
        return pickup.parse_pickup_response(response, self.settings) 
