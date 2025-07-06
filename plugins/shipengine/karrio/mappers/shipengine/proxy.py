"""Karrio ShipEngine client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.shipengine.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Request shipping rates from multiple carriers via ShipEngine."""

        response = lib.request(
            url=f"{self.settings.server_url}/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self.settings.auth_headers,
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create a shipping label via ShipEngine."""

        response = lib.request(
            url=f"{self.settings.server_url}/labels",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self.settings.auth_headers,
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """Get tracking information for shipments."""

        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/tracking",
                params={"tracking_number": tracking_number},
                trace=self.trace_as("json"),
                method="GET",
                headers=self.settings.auth_headers,
            )

        # Extract tracking numbers from request data
        request_data = request.serialize()
        tracking_numbers = request_data.get("trackingNumbers", []) if isinstance(request_data, dict) else request_data
        
        # Use concurrent requests for multiple tracking numbers
        responses = lib.run_concurently(_get_tracking, tracking_numbers)

        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Validate addresses using ShipEngine."""

        response = lib.request(
            url=f"{self.settings.server_url}/addresses/validate",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers=self.settings.auth_headers,
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel a shipment label."""

        data = request.serialize()
        label_id = data.get("label_id")

        response = lib.request(
            url=f"{self.settings.server_url}/labels/{label_id}/void",
            trace=self.trace_as("json"),
            method="PUT",
            headers=self.settings.auth_headers,
        )

        return lib.Deserializable(response, lib.to_dict)
    