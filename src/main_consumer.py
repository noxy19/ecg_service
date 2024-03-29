from src.application.process_ecg_use_case import ProcessEcgUseCase
from src.infrastructure import providers
from src.infrastructure.postgres_repository import PostgresEcgRepository
from typing import Protocol
from src.logger_config import setup_global_logger
from src.domain.count_zero_crossings_service import CountZeroCrossingsService
from src.domain.messages import PostEcgEvent
import logging
from result import Result, Ok
import asyncio
from aiobotocore.session import get_session  # type: ignore[import-untyped]
import json
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger()


class Processor(Protocol):
    async def execute(self, event: PostEcgEvent) -> Result[None, Exception]:
        pass


class SqsPoller:
    def __init__(
        self,
        processor: Processor,
        queue_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = "us-east-1",
        aws_endpoint_url: str | None = None,
    ):
        self._processor = processor
        self._queue_url = queue_url
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._region_name = region_name
        self._aws_endpoint_url = aws_endpoint_url
        self._back_off_time = 5

    async def _is_queue_created(self, client):
        response = await client.list_queues()
        queues_urls = response.get("QueueUrls", [])
        return any(self._queue_url == url for url in queues_urls)

    async def run(self):
        session = get_session()
        async with session.create_client(
            "sqs",
            endpoint_url=self._aws_endpoint_url,
            region_name=self._region_name,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        ) as client:
            while True:
                if not await self._is_queue_created(client):
                    logger.warning("Queue not found, retrying")
                    await asyncio.sleep(1)
                    continue

                response = await client.receive_message(
                    QueueUrl=self._queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=20
                )

                messages = response.get("Messages", [])

                for message in messages:
                    logger.info(f"Processing message {message['MessageId']}: {message['Body']}")
                    event = PostEcgEvent.parse_obj(json.loads(message["Body"]))

                    result = await self._processor.execute(event)

                    if isinstance(result, Ok):
                        await client.delete_message(QueueUrl=self._queue_url, ReceiptHandle=message["ReceiptHandle"])
                    else:
                        await asyncio.sleep(self._back_off_time)


async def main():
    setup_global_logger()
    settings = providers.settings_provider()
    zero_crossings_service = CountZeroCrossingsService()
    connectionPool = AsyncConnectionPool(
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}@db", max_size=10
    )
    repository = PostgresEcgRepository(connectionPool)
    processor = ProcessEcgUseCase(zero_crossings_service, repository)
    poller = SqsPoller(
        processor=processor,
        queue_url=settings.queue_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.region_name,
        aws_endpoint_url=settings.aws_endpoint_url,
    )
    await poller.run()


if __name__ == "__main__":
    asyncio.run(main())
