from typing import List, Tuple
from karrio.core.utils.serializable import Serializable, Deserializable
from karrio.api.mapper import Mapper as BaseMapper
from karrio.core.models import (
    TrackingRequest,
    #
    TrackingDetails,
    Message,
)
from karrio.providers.dicom import (
    parse_tracking_response,
    #
    tracking_request,
)
from karrio.mappers.dicom.settings import Settings


class Mapper(BaseMapper):
    settings: Settings


    def create_tracking_request(self, payload: TrackingRequest) -> Serializable:
        return tracking_request(payload, self.settings)

    #
    #
    #
    #

    #
    #
    #
    #
    #

    def parse_tracking_response(
        self, response: Deserializable
    ) -> Tuple[List[TrackingDetails], List[Message]]:
        return parse_tracking_response(response, self.settings)
