from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, APIRouter
from .jwt_auth import get_current_user, JwtClaims
from .providers import create_ecg_use_case_provider
from src.application.create_ecg_use_case import CreateEcgUseCase
from src.domain.model import Electrocardiogram, ElectrocardiogramLead, LeadType
import logging
from uuid import UUID, uuid4
from result import Ok, Err
from fastapi import HTTPException


class ElectrocardiogramLeadDto(BaseModel):
    name: LeadType
    num_samples: Optional[int]
    signal: list[int]


class ElectrocardiogramDto(BaseModel):
    id: UUID
    date: str
    leads: list[ElectrocardiogramLeadDto]


router = APIRouter()
logger = logging.getLogger()


def from_dto_to_domain(ecg_dto: ElectrocardiogramDto, user_id: UUID) -> Electrocardiogram:
    return Electrocardiogram(
        id=ecg_dto.id,
        user_id=user_id,
        date=ecg_dto.date,
        leads=[
            ElectrocardiogramLead(name=lead.name, num_samples=lead.num_samples, signal=lead.signal)
            for lead in ecg_dto.leads
        ],
    )


@router.post("/electrocardiograms", status_code=202)
async def post_electrocardiogram(
    ecg_dto: ElectrocardiogramDto,
    user: JwtClaims = Depends(get_current_user),
    use_case: CreateEcgUseCase = Depends(create_ecg_use_case_provider),
):
    logger.info("endpoint entry")
    ecg = from_dto_to_domain(ecg_dto=ecg_dto, user_id=user.sub)
    result = await use_case.execute(ecg)
    if isinstance(result, Ok):
        return {"message": "ECG processing accepted", "ecgId": ecg.id}
    else:
        request_id = uuid4()
        logger.error(f"Error processing request {request_id}: {result.err()}")
        raise HTTPException(
            status_code=400, detail=f"Error processing the ECG, contact support with this request id: {request_id}"
        )
