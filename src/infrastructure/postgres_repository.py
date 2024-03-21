from result import Result
from uuid import UUID
from src.domain.model import Electrocardiogram, EcgLeadInsight, User
from src.domain.repository import EcgRepository
from psycopg_pool import AsyncConnectionPool
from result import Ok, Err
import asyncio


class PostgresEcgRepository(EcgRepository):
    def __init__(self, connection_pool: AsyncConnectionPool):
        self._connection_pool = connection_pool

    async def save(self, ecg: Electrocardiogram, lead_insights: list[EcgLeadInsight]) -> Result[None, Exception]:
        try:
            async with self._connection_pool.connection() as conn:
                await conn.execute(
                    "INSERT into ecgs(id, date_created, user_id) values(%s, %s, %s)", (ecg.id, ecg.date, ecg.user_id)
                )

                asyncio.gather(
                    *[
                        asyncio.create_task(
                            conn.execute(
                                "INSERT into leads(ecg_id, name, number_of_samples, signal) values(%s, %s, %s, %s)",
                                (ecg.id, lead.name, lead.num_samples, lead.signal),
                            )
                        )
                        for lead in ecg.leads
                    ]
                )

                asyncio.gather(
                    *[
                        asyncio.create_task(
                            conn.execute(
                                "INSERT into insights(ecg_id, lead_name, crossings) values(%s, %s, %s)",
                                (insight.ecg_id, insight.lead_name, insight.zero_crossings),
                            )
                        )
                        for insight in lead_insights
                    ]
                )
                await conn.commit()
            return Ok(None)
        except Exception as e:
            return Err(e)

    async def find_by_id(self, ecg_id: UUID, user_id: UUID) -> Result[list[EcgLeadInsight], Exception]:
        try:
            async with self._connection_pool.connection() as conn:
                cursor = conn.cursor()
                await cursor.execute(
                    "SELECT ins.ecg_id, ins.lead_name, ins.crossings FROM insights ins JOIN ecgs e ON ins.ecg_id = e.id WHERE e.id = %s AND e.user_id = %s;",
                    (ecg_id, user_id),
                )
                result = await cursor.fetchall()

                insights = [
                    EcgLeadInsight(ecg_id=insight[0], lead_name=insight[1], zero_crossings=insight[2])
                    for insight in result
                ]

            return Ok(insights)
        except Exception as e:
            return Err(e)

    async def create_user(self, user_id: UUID, username: str, hashed_password: str) -> Result[None, Exception]:
        try:
            async with self._connection_pool.connection() as conn:
                await conn.execute(
                    "INSERT into users(id, username, password_hash) values(%s, %s, %s)",
                    (user_id, username, hashed_password),
                )
                await conn.commit()
            return Ok(None)
        except Exception as e:
            return Err(e)

    async def find_user_hashpass(self, username: str) -> Result[User, Exception]:
        try:
            async with self._connection_pool.connection() as conn:
                cursor = conn.cursor()
                await cursor.execute(
                    "SELECT id, password_hash from users where username = %s",
                    [username],
                )
                result = await cursor.fetchall()
                return Ok(User(id=result[0][0], username=username, hashed_password=result[0][1]))
        except Exception as e:
            return Err(e)
