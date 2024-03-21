import logging
from result import Result, Ok
from src.domain.count_zero_crossings_service import CountZeroCrossingsService
from src.domain.messages import PostEcgEvent
from src.domain.model import EcgLeadInsight
from src.domain.repository import EcgRepository
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger()


class ProcessEcgUseCase:

    def __init__(self, zero_crossings: CountZeroCrossingsService, repository: EcgRepository):
        self._zero_crossings = zero_crossings
        self._repository = repository

    async def execute(self, event: PostEcgEvent) -> Result[None, Exception]:
        lead_insights = [
            EcgLeadInsight(
                ecg_id=event.electrocardiogram.id,
                lead_name=lead.name,
                zero_crossings=self._zero_crossings.count(lead.signal),
            )
            for lead in event.electrocardiogram.leads
        ]
        result = await self._repository.save(event.electrocardiogram, lead_insights)
        return Ok(None)
