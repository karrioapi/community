"""Karrio Easyship client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.easyship.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Return the access_token for API authentication.

        Easyship uses a direct access token (no OAuth flow required).
        This method provides a consistent interface with other carriers.
        """
        return lib.Deserializable(self.settings.access_token)

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/2023-01/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        # create shipment with retry for transient failures (e.g., Cloudflare 522 timeouts)
        response = lib.request(
            url=f"{self.settings.server_url}/2023-01/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
            max_retries=2,
        )

        return lib.Deserializable(response, lib.to_dict_safe, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        easyship_shipment_id = request.serialize().get("easyship_shipment_id")
        response = lib.request(
            url=f"{self.settings.server_url}/2023-01/shipments/{easyship_shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        responses = lib.run_asynchronously(
            lambda data: (
                data["shipment_id"],
                lib.request(
                    url=f"{self.settings.server_url}/2023-01/shipments/{data['shipment_id']}",
                    trace=self.trace_as("json"),
                    method="GET",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                        "user-agent": "app/1.0",
                    },
                ),
            ),
            [_ for _ in request.serialize() if _.get("shipment_id")],
        )

        return lib.Deserializable(
            responses,
            lambda __: [(_[0], lib.to_dict(_[1])) for _ in __],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/2023-01/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx))

        if response.deserialize() is not None:
            response = self.schedule_pickup(request)

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        easyship_pickup_id = request.serialize().get("easyship_pickup_id")
        response = lib.request(
            url=f"{self.settings.server_url}/2023-01/pickups/{easyship_pickup_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "user-agent": "app/1.0",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_manifest(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        # create manifest
        response = lib.to_dict(
            lib.request(
                url=f"{self.settings.server_url}/2023-01/manifests",
                data=lib.to_json(request.serialize()),
                trace=self.trace_as("json"),
                method="POST",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "user-agent": "app/1.0",
                },
            )
        )

        # extract manifest url
        manifest_url = lib.failsafe(lambda: response["manifest"]["document"]["url"])

        # download manifest file
        response.update(
            manifest_file=lib.identity(
                None
                if manifest_url is None
                else lib.request(
                    url=manifest_url,
                    method="GET",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "origin": "http://localhost:5002",
                        "user-agent": "app/1.0",
                    },
                    decoder=lib.encode_base64,
                )
            )
        )

        return lib.Deserializable(response)
