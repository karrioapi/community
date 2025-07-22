"""Karrio DHL eCommerce Americas client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.dhl_ecommerce_americas.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def _get_access_token(self):
        """Get OAuth access token from DHL API."""
        auth_url = f"{self.settings.server_url}/rest/v1/OAuth/AccessToken"
        params = {
            "clientId": self.settings.client_id,
            "password": self.settings.password,
            "returnFormat": "json"
        }
        
        try:
            response = lib.request(
                url=auth_url,
                method="GET",
                params=params,
                trace=self.trace_as("json"),
            )
            
            data = lib.to_dict(response)
            return data.get("authToken", "")
        except Exception as e:
            # If authentication fails, return empty token
            # Error will be handled in the actual API call
            return ""

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        token = self._get_access_token()
        response = lib.request(
            url=f"{self.settings.server_url}/rest/v2/rates",
            data=request.serialize(),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        token = self._get_access_token()
        tracking_numbers = request.serialize()
        if isinstance(tracking_numbers, list):
            tracking_number = tracking_numbers[0] if tracking_numbers else ""
        else:
            tracking_number = tracking_numbers.get("trackingNumbers", [""])[0]
            
        response = lib.request(
            url=f"{self.settings.server_url}/rest/v2/tracking/{tracking_number}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        token = self._get_access_token()
        
        # Set access token in request header
        request_data = request.serialize()
        if "header" in request_data:
            request_data["header"]["accessToken"] = token
        
        response = lib.request(
            url=f"{self.settings.server_url}/rest/v2/label",
            data=request_data,
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        token = self._get_access_token()
        shipment_id = request.serialize().get("shipment_id")
        response = lib.request(
            url=f"{self.settings.server_url}/rest/v2/shipment/{shipment_id}/cancel",
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        return lib.Deserializable(response, lib.to_dict)
