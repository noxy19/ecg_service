from abc import ABC, abstractmethod
from result import Result
from uuid import UUID
from .model import Electrocardiogram, EcgLeadInsight, User


class EcgRepository(ABC):
    @abstractmethod
    async def save(self, ecg: Electrocardiogram, lead_insights: list[EcgLeadInsight]) -> Result[None, Exception]:
        pass

    @abstractmethod
    async def find_by_id(self, ecg_id: UUID, user_id: UUID) -> Result[list[EcgLeadInsight], Exception]:
        pass

    @abstractmethod
    async def create_user(self, user_id: UUID, username: str, hashed_password: str) -> Result[None, Exception]:
        pass

    @abstractmethod
    async def find_user_hashpass(self, username: str) -> Result[User, Exception]:
        pass
