from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class AgeGroupBase(BaseModel):
    """Schema base para faixas etárias."""
    name: str = Field(..., description="Nome da faixa etária")
    min_age: int = Field(..., ge=0, description="Idade mínima inclusiva")
    max_age: int = Field(..., ge=0, description="Idade máxima inclusiva")


class AgeGroupCreate(AgeGroupBase):
    """Schema para criação de faixas etárias."""
    pass


class AgeGroupRead(AgeGroupBase):
    """Schema para leitura de faixas etárias com ID."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID


class AgeGroupUpdate(BaseModel):
    """Schema para atualização parcial de faixas etárias."""
    name: Optional[str] = Field(None, description="Nome da faixa etária")
    min_age: Optional[int] = Field(None, ge=0, description="Idade mínima inclusiva")
    max_age: Optional[int] = Field(None, ge=0, description="Idade máxima inclusiva")
