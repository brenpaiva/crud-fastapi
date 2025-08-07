from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class AgeGroupBase(BaseModel):
    name: str = Field(..., description="Nome da faixa etária")
    min_age: int = Field(..., ge=0, description="Idade mínima inclusiva")
    max_age: int = Field(..., ge=0, description="Idade máxima inclusiva")

class AgeGroupCreate(AgeGroupBase):
    pass

class AgeGroupRead(AgeGroupBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class AgeGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome da faixa etária")
    min_age: Optional[int] = Field(None, ge=0, description="Idade mínima inclusiva")
    max_age: Optional[int] = Field(None, ge=0, description="Idade máxima inclusiva")
