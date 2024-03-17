import logging
from result import Result, Ok
from src.domain.count_zero_crossings_service import CountZeroCrossingsService
from src.domain.messages import PostEcgEvent

logger = logging.getLogger()


class ProcessEcgUseCase:

    def __init__(self, zero_crossings: CountZeroCrossingsService):
        self._zero_crossings = zero_crossings

    async def execute(self, event: PostEcgEvent) -> Result[None, Exception]:
        logger.info("ProcessEcgUseCase event recieved")
        for lead in event.electrocardiogram.leads:
            zero_crossings = self._zero_crossings.count(lead.signal)
            logger.info(f'ZERO CROSSINGS: {zero_crossings}, for lead {lead.name}')

        # db call
        return Ok(None)
