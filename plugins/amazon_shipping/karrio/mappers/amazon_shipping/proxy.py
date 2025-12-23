import typing
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.providers.amazon_shipping.error as provider_error
from karrio.mappers.amazon_shipping.settings import Settings


class Proxy(proxy.Proxy):
    settings: Settings

    def authenticate(self, _=None) -> lib.Deserializable[str]:
        """Retrieve the access_token using the seller_id|developer_id pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.seller_id}|{self.settings.developer_id}"

        def get_token():
            query = urllib.parse.urlencode(
                dict(
                    developerId=self.settings.developer_id,
                    sellingPartnerId=self.settings.seller_id,
                    mwsAuthToken=self.settings.mws_auth_token,
                )
            )
            result = lib.request(
                url=f"{self.settings.server_url}/authorization/v1/authorizationCode?{query}",
                trace=self.settings.trace_as("json"),
                method="POST",
                headers={"content-Type": "application/json"},
                max_retries=2,
            )

            response = lib.to_dict(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages)

            # Validate that authorizationCode is present in the response payload
            authorization_code = lib.failsafe(
                lambda: response.get("payload", {}).get("authorizationCode")
            )
            if not authorization_code:
                raise errors.ParsedMessagesError(
                    messages=[
                        models.Message(
                            carrier_name=self.settings.carrier_name,
                            carrier_id=self.settings.carrier_id,
                            message="Authentication failed: No authorization code received",
                            code="AUTH_ERROR",
                        )
                    ]
                )

            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 0))
            )

            return {
                **response,
                "expiry": lib.fdatetime(expiry),
                "authorizationCode": authorization_code,
            }

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="authorizationCode",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path="/shipping/v1/rates",
            request=lib.Serializable(request, lib.to_json),
        )

        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path="/shipping/v1/purchaseShipment",
            request=lib.Serializable(request, lib.to_json),
        )

        return lib.Deserializable(response, lib.to_dict)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = self._send_request(
            path=f"/shipping/v1/shipments/{request.serialize()}/cancel",
        )

        return lib.Deserializable(response if any(response) else "{}", lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate().deserialize()

        track = lambda trackingId: (
            trackingId,
            lib.request(
                url=f"{self.settings.server_url}/shipping/v1/tracking/{trackingId}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Content-Type": "application/json",
                    "x-amz-access-token": access_token,
                },
            ),
        )

        responses: typing.List[typing.Tuple[str, str]] = lib.run_asynchronously(
            track, request.serialize()
        )
        return lib.Deserializable(
            responses,
            lambda res: [(key, lib.to_dict(response)) for key, response in res],
        )

    def _send_request(
        self, path: str, request: lib.Serializable = None, method: str = "POST"
    ) -> str:
        access_token = self.authenticate().deserialize()
        data: dict = dict(data=request.serialize()) if request is not None else dict()
        return lib.request(
            **{
                "url": f"{self.settings.server_url}{path}",
                "trace": self.trace_as("json"),
                "method": method,
                "headers": {
                    "Content-Type": "application/json",
                    "x-amz-access-token": access_token,
                },
                **data,
            }
        )
