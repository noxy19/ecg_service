from uuid import UUID
from .model import Electrocardiogram
from dataclasses import asdict
from typing import Dict, Any
from pydantic import BaseModel


class PostEcgEvent(BaseModel):
    id: UUID
    electrocardiogram: Electrocardiogram

    def to_json(self) -> str:
        return self.json()
