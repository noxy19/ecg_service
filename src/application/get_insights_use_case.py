from uuid import UUID
from src.domain.repository import EcgRepository
from src.domain.model import EcgLeadInsight
from result import Result


class GetInsightsUseCase:

    def __init__(self, repository: EcgRepository):
        self._repository = repository

    async def execute(self, ecg_id: UUID, user_id: UUID) -> Result[list[EcgLeadInsight], Exception]:
        insights = await self._repository.find_by_id(ecg_id=ecg_id, user_id=user_id)
        return insights
