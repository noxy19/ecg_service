from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict
from uuid import UUID
from result import Result


class Event(Protocol):
    id: UUID

    def to_json(self) -> str:
        pass


class MessageService(ABC):

    @abstractmethod
    async def publish(self, event: Event) -> Result[None, Exception]:
        pass
