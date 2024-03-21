from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel
import jwt
from src.application.settings import Settings
from .providers import settings_provider
import logging
from uuid import UUID
import bcrypt

logger = logging.getLogger()
security = HTTPBearer()


class JwtClaims(BaseModel):
    name: str
    sub: UUID


def decode_jwt(token: str, secret_key: str, algorithm: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_token if decoded_token else None
    except jwt.PyJWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security), settings: Settings = Depends(settings_provider)
) -> JwtClaims:
    try:
        token = credentials.credentials
        decoded_token = decode_jwt(token, settings.jwt_secret_key, settings.jwt_algorithm)
        return JwtClaims.parse_obj(decoded_token)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


async def is_admin_user_valid(
    credentials: HTTPAuthorizationCredentials = Security(security), settings: Settings = Depends(settings_provider)
) -> bool:
    hashed = bcrypt.hashpw(settings.admin_password.encode("utf-8"), bcrypt.gensalt())
    provided_password = credentials.credentials
    return bcrypt.checkpw(provided_password.encode("utf-8"), hashed)
