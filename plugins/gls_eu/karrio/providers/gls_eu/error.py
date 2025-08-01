import typing
import karrio.core.models as models
import karrio.core.utils as utils


def parse_error_response(
    response: dict,
    settings: utils.Settings,
) -> typing.List[models.Message]:
    errors = []
    
    if "errors" in response:
        for error in response["errors"]:
            errors.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=error.get("code"),
                    message=error.get("message"),
                    details=error,
                )
            )

    return errors 
