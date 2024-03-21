import bcrypt
from src.domain.repository import EcgRepository
from typing import Protocol
from uuid import uuid4
from result import Result, Ok, Err
import datetime
from src.application.settings import Settings
import jwt


class UserCommand(Protocol):
    username: str
    password: str


class UserUseCase:

    def __init__(self, repository: EcgRepository, settings: Settings):
        self._repository = repository
        self._settings = settings

    async def create(self, command: UserCommand) -> Result[None, Exception]:
        hashed_password = self._hash_password(command.password)
        user_id = uuid4()
        return await self._repository.create_user(
            user_id=user_id, username=command.username, hashed_password=hashed_password
        )

    async def login(self, command: UserCommand) -> Result[str, Exception]:
        result = await self._repository.find_user_hashpass(username=command.username)

        if isinstance(result, Ok):
            user = result.ok()
            if bcrypt.checkpw(command.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
                payload = {
                    "sub": str(user.id),
                    "name": user.username,
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60000),
                }

                token = jwt.encode(payload, self._settings.jwt_secret_key, algorithm=self._settings.jwt_algorithm)
                return Ok(token)
            return Err(Exception("Wrong user or password"))
        return result

    def _hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")
