from src.domain.message_service import MessageService, Event
from aiobotocore.session import get_session  # type: ignore[import-untyped]
import json
import dataclasses
from src.application.settings import Settings
from result import Result, Ok, Err


class SqsMessageService(MessageService):
    def __init__(
        self,
        queue_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = "us-east-1",
        aws_endpoint_url: str | None = None,
    ):
        self._queue_url = queue_url
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._region_name = region_name
        self._aws_endpoint_url = aws_endpoint_url

    async def publish(self, event: Event) -> Result[None, Exception]:
        try:
            session = get_session()
            async with session.create_client(
                "sqs",
                endpoint_url=self._aws_endpoint_url,
                region_name=self._region_name,
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
            ) as client:
                message_body = event.to_json()
                await client.send_message(QueueUrl=self._queue_url, MessageBody=message_body)
                return Ok(None)
        except Exception as e:
            return Err(e)
