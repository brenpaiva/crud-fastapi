from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.models.enrollment import EnrollmentStatus


class EnrollmentBase(BaseModel):
    """Schema base para inscrições."""
    name: str = Field(..., description="Nome completo do inscrito")
    email: str = Field(..., description="Email de contato")
    age: int = Field(..., ge=0, le=120, description="Idade atual")


class EnrollmentCreate(EnrollmentBase):
    """Schema para criação de inscrições."""
    age_group_id: UUID = Field(..., description="ID da faixa etária")


class EnrollmentRead(EnrollmentBase):
    """Schema para leitura de inscrições com ID e status."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    age_group_id: UUID
    status: EnrollmentStatus


class EnrollmentUpdateStatus(BaseModel):
    """Schema para atualização do status de inscrições."""
    status: EnrollmentStatus = Field(..., description="Novo status da inscrição")