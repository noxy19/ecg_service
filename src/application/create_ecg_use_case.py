from result import Result, Ok, Err
from src.domain.message_service import MessageService
from src.domain.model import Electrocardiogram
from src.domain.messages import PostEcgEvent
from uuid import uuid4


class CreateEcgUseCase:
    def __init__(self, message_service: MessageService):
        self._message_service = message_service

    async def execute(self, electrocardiogram: Electrocardiogram) -> Result[None, Exception]:
        event_id = uuid4()
        event = PostEcgEvent(id=event_id, electrocardiogram=electrocardiogram)
        return await self._message_service.publish(event)
