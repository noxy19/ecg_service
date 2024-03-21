from src.application.settings import Settings
from src.domain.message_service import MessageService
from src.domain.repository import EcgRepository
from src.infrastructure.sqs_message_service import SqsMessageService
from src.application.create_ecg_use_case import CreateEcgUseCase
from src.application.get_insights_use_case import GetInsightsUseCase
from src.application.user_use_case import UserUseCase
from src.infrastructure.postgres_repository import PostgresEcgRepository
from fastapi import Depends
from psycopg_pool import AsyncConnectionPool


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


async def repository_provider(settings: Settings = Depends(settings_provider)) -> EcgRepository:
    connectionPool = AsyncConnectionPool(f"postgresql://{settings.postgres_user}:{settings.postgres_password}@db")
    return PostgresEcgRepository(connectionPool)


def create_ecg_use_case_provider(
    message_service: MessageService = Depends(message_service_provider),
) -> CreateEcgUseCase:
    return CreateEcgUseCase(message_service=message_service)


def get_insights_use_case_provider(repository: EcgRepository = Depends(repository_provider)) -> GetInsightsUseCase:
    return GetInsightsUseCase(repository)


def user_use_case_provider(
    repository: EcgRepository = Depends(repository_provider), settings: Settings = Depends(settings_provider)
) -> UserUseCase:
    return UserUseCase(repository, settings)
