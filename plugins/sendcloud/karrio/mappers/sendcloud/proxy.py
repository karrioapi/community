"""Karrio SendCloud client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.sendcloud.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/shipping-products",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {lib.encode_base64(f'{self.settings.username}:{self.settings.password}')}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        # create shipment
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/parcels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {lib.encode_base64(f'{self.settings.username}:{self.settings.password}')}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        sendcloud_parcel_id = request.serialize().get("sendcloud_parcel_id")
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/parcels/{sendcloud_parcel_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Basic {lib.encode_base64(f'{self.settings.username}:{self.settings.password}')}",
                "Content-Type": "application/json",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        responses = lib.run_asynchronously(
            lambda data: (
                data["tracking_number"],
                lib.request(
                    url=f"{self.settings.server_url}/api/v2/parcels/{data['tracking_number']}",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Authorization": f"Basic {lib.encode_base64(f'{self.settings.username}:{self.settings.password}')}",
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
