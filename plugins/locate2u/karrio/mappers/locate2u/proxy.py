"""Karrio Locate2u client proxy."""

import base64
import typing
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.locate2u.error as provider_error
import karrio.mappers.locate2u.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.client_id}|{self.settings.client_secret}"

        def get_token():
            pair = "%s:%s" % (self.settings.client_id, self.settings.client_secret)
            authorization = base64.b64encode(pair.encode("utf-8")).decode("ascii")

            result = lib.request(
                url=f"{self.settings.auth_server_url}/connect/token",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={
                    "content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {authorization}",
                },
                data=urllib.parse.urlencode(
                    dict(
                        scope="locate2u.api",
                        grant_type="client_credentials",
                    )
                ),
                max_retries=2,
            )

            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages)

            # Validate that access_token is present in the response
            if "access_token" not in response:
                raise errors.ParsedMessagesError(
                    messages=[
                        models.Message(
                            carrier_name=self.settings.carrier_name,
                            carrier_id=self.settings.carrier_id,
                            message="Authentication failed: No access token received",
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
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/stops",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            on_error=provider_error.parse_http_response,
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()
        payload = request.serialize()
        response = lib.request(
            url=f"{self.settings.server_url}/api/v1/stops/{payload['stopId']}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            on_error=provider_error.parse_http_response,
            decoder=lambda _: dict(ok=True),
        )

        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable[str]:
        access_token = self.authenticate().deserialize()

        def _get_tracking(stop_id: str):
            return stop_id, lib.request(
                url=f"{self.settings.server_url}/api/v1/stops/{stop_id}?includeItems=false&includeLines=false",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
                on_error=provider_error.parse_http_response,
            )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_concurently(
            _get_tracking, request.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(track)) for num, track in res if any(track.strip())
            ],
        )
