"""Karrio eShipper client proxy."""

import datetime
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.eshipper.error as provider_error
import karrio.mappers.eshipper.settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the token using the principal|credential pair
        or collect it from the cache if an unexpired token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.principal}|{self.settings.credential}"

        def get_token():
            result = lib.request(
                url=f"{self.settings.server_url}/api/v2/authenticate",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={"content-Type": "application/json"},
                data=lib.to_json(
                    {
                        "principal": self.settings.principal,
                        "credential": self.settings.credential,
                    }
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            # Validate that token is present in the response
            if "token" not in response:
                raise errors.ParsedMessagesError(
                    messages=[
                        models.Message(
                            carrier_name=self.settings.carrier_name,
                            carrier_id=self.settings.carrier_id,
                            message="Authentication failed: No token received",
                            code="AUTH_ERROR",
                        )
                    ]
                )

            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 0))
            )

            return {**response, "expiry": lib.fdatetime(expiry)}

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="token",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/quote",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/ship",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="PUT",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/ship/cancel",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        query = lib.to_query_string(request.serialize())
        response = lib.request(
            url=f"{self.settings.server_url}/api/v2/track/events?{query}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

        return lib.Deserializable(response, lib.to_dict)
