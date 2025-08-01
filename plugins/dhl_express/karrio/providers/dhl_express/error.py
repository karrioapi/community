import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_express.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses: typing.List[dict] = []
    
    if isinstance(response, dict):
        if "status" in response and response.get("status") != "SUCCESS":
            responses.append({
                "code": response.get("status"),
                "message": response.get("message", "Unknown error"),
                "detail": response.get("detail", "")
            })
        elif "errors" in response:
            responses.extend(response["errors"])
        elif "error" in response:
            error = response["error"]
            responses.append({
                "code": error.get("code", "UNKNOWN"),
                "message": error.get("message", "Unknown error"),
                "detail": error.get("detail", "")
            })
        elif response.get("message"):
            responses.append({
                "code": "ERROR",
                "message": response.get("message"),
                "detail": response.get("detail", "")
            })

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code", "UNKNOWN"),
            message=error.get("message", "Unknown error"),
            details={
                **kwargs,
                **({"detail": error.get("detail")} if error.get("detail") else {}),
            },
        )
        for error in responses
    ]
