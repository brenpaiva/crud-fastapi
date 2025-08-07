from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.enrollment import EnrollmentStatus

class EnrollmentBase(BaseModel):
    name: str = Field(..., description="Nome completo do inscrito")
    age: int = Field(..., ge=0, description="Idade informada para validação de faixa")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do inscrito")

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(EnrollmentBase):
    id: UUID
    age_group_id: UUID
    status: EnrollmentStatus
    requested_at: datetime
    processed_at: Optional[datetime]

class EnrollmentUpdateStatus(BaseModel):
    status: EnrollmentStatus = Field(..., description="Novo status da inscrição")