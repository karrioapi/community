"""Karrio SAPIENT client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.providers.sapient.error as provider_error
import karrio.mappers.sapient.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = (
            f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"
        )

        def get_token():
            response = lib.request(
                url=f"https://authentication.intersoftsapient.net/connect/token",
                method="POST",
                headers={
                    "content-Type": "application/x-www-form-urlencoded",
                    "user-agent": "Karrio/1.0",
                },
                data=lib.to_query_string(
                    dict(
                        grant_type="client_credentials",
                        client_id=self.settings.client_id,
                        client_secret=self.settings.client_secret,
                    )
                ),
                decoder=lib.to_dict,
                max_retries=2,
            )

            messages = provider_error.parse_error_response(response, self.settings)
            if any(messages):
                raise errors.ParsedMessagesError(messages)

            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 0))
            )
            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=10,
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/v4/shipments/{request.ctx['carrier_code']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "user-agent": "Karrio/1.0",
            },
            decoder=lib.to_dict_safe,
            on_error=lambda b: lib.to_dict_safe(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/v4/shipments/status",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "user-agent": "Karrio/1.0",
            },
            on_ok=lambda _: '{"ok": true}',
            decoder=lib.to_dict_safe,
            on_error=lambda b: lib.to_dict_safe(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)

    def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/v4/collections/{request.ctx['carrier_code']}/{request.ctx['shipmentId']}",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "user-agent": "Karrio/1.0",
            },
            decoder=lib.to_dict_safe,
            on_error=lambda b: lib.to_dict_safe(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        response = self.cancel_pickup(lib.Serializable(request.ctx))

        if response.deserialize().get("ok"):
            response = self.schedule_pickup(request)

        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate(request).deserialize()
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/v4/collections/{payload['carrier_code']}/{payload['shipmentId']}/cancel",
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "user-agent": "Karrio/1.0",
            },
            decoder=lib.to_dict_safe,
            on_error=lambda b: lib.to_dict_safe(b.read()),
        )

        return lib.Deserializable(response, lib.to_dict)
