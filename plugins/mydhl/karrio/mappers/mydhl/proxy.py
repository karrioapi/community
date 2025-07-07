"""Karrio MyDHL client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.mydhl.settings as provider_settings

class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Get rates using POST /rates for multi-piece shipments."""
        response = lib.request(
            url=f"{self.settings.server_url}/mydhlapi/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create shipment using POST /shipments."""
        response = lib.request(
            url=f"{self.settings.server_url}/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel shipment using DELETE /shipments/{shipmentTrackingNumber}."""
        data = request.serialize()
        shipment_id = data.get("shipmentIdentifier") or data.get("shipmentId") or data.get("shipmentTrackingNumber")
        
        response = lib.request(
            url=f"{self.settings.server_url}/shipments/{shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """Get tracking using GET /tracking with tracking numbers."""
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/tracking",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Authorization": f"Basic {self.settings.authorization}",
                    "Accept": "application/json",
                },
            )

        data = request.serialize()
        tracking_numbers = data.get("trackingNumbers", [])
        responses = lib.run_concurently(_get_tracking, tracking_numbers)
        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Schedule pickup using POST /pickups."""
        response = lib.request(
            url=f"{self.settings.server_url}/mydhlapi/pickups",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Update pickup using PATCH /pickups/{dispatchConfirmationNumber}."""
        data = request.serialize()
        dispatch_confirmation_number = data.get("dispatchConfirmationNumber")

        response = lib.request(
            url=f"{self.settings.server_url}/mydhlapi/pickups/{dispatch_confirmation_number}",
            data=lib.to_json(data),
            trace=self.trace_as("json"),
            method="PATCH",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel pickup using DELETE /pickups/{dispatchConfirmationNumber}."""
        data = request.serialize()
        dispatch_confirmation_number = data.get("dispatchConfirmationNumber")
        requestor_name = data.get("requestorName", "System")
        reason = data.get("reason", "Customer request")

        response = lib.request(
            url=f"{self.settings.server_url}/mydhlapi/pickups/{dispatch_confirmation_number}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
            params={
                "requestorName": requestor_name,
                "reason": reason,
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def validate_address(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Validate address using GET /address-validate."""
        data = request.serialize()

        response = lib.request(
            url=f"{self.settings.server_url}/mydhlapi/address-validate",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Basic {self.settings.authorization}",
                "Accept": "application/json",
            },
            params=data,
        )
        return lib.Deserializable(response, lib.to_dict)