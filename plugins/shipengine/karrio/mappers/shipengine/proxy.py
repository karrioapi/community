"""Karrio ShipEngine client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.shipengine.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "API-Key": self.settings.api_key,
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # create label (shipment)
        response = lib.request(
            url=f"{self.settings.server_url}/v1/labels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "API-Key": self.settings.api_key,
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        shipengine_label_id = request.serialize().get("shipengine_label_id")
        response = lib.request(
            url=f"{self.settings.server_url}/v1/labels/{shipengine_label_id}/void",
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "API-Key": self.settings.api_key,
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda data: (
                data["tracking_number"],
                lib.request(
                    url=f"{self.settings.server_url}/v1/tracking",
                    data=lib.to_json(data),
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "API-Key": self.settings.api_key,
                        "Content-Type": "application/json",
                    },
                ),
            ),
            [_ for _ in request.serialize() if _.get("tracking_number")],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        ) 
