from src.application.settings import Settings
from src.domain.message_service import MessageService
from src.infrastructure.sqs_message_service import SqsMessageService
from src.application.create_ecg_use_case import CreateEcgUseCase
from fastapi import Depends


def settings_provider() -> Settings:
    return Settings()  # type: ignore[call-arg]


def message_service_provider(settings: Settings = Depends(settings_provider)) -> MessageService:
    return SqsMessageService(
        queue_url=settings.queue_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.region_name,
        aws_endpoint_url=settings.aws_endpoint_url,
    )


def create_ecg_use_case_provider(
    message_service: MessageService = Depends(message_service_provider),
) -> CreateEcgUseCase:
    return CreateEcgUseCase(message_service=message_service)
