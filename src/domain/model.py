from typing import Optional, Literal
from uuid import UUID
from dataclasses import dataclass
from pydantic import BaseModel


LeadType = Literal["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]


class ElectrocardiogramLead(BaseModel):
    name: LeadType
    num_samples: Optional[int]
    signal: list[int]


class Electrocardiogram(BaseModel):
    id: UUID
    user_id: UUID
    date: str
    leads: list[ElectrocardiogramLead]


class EcgLeadInsight(BaseModel):
    ecg_id: UUID
    lead_name: LeadType
    zero_crossings: int


class User(BaseModel):
    id: UUID
    username: str
    hashed_password: str
