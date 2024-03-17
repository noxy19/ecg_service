from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    jwt_secret_key: str = Field()
    jwt_algorithm: str = Field("HS256")
    aws_endpoint_url: str | None = Field(None)
    queue_url: str = Field()
    aws_access_key_id: str = Field()
    aws_secret_access_key: str = Field()
    region_name: str = Field()
