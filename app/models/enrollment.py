from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.age_group import AgeGroup

class EnrollmentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(..., description="Nome completo do inscrito")
    age: int = Field(..., ge=0, description="Idade informada para validação de faixa")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do inscrito, formatado ou não")
    age_group_id: Optional[UUID] = Field(
        default=None, foreign_key="age_groups.id", description="FK para a faixa etária correspondente"
    )
    status: EnrollmentStatus = Field(
        default=EnrollmentStatus.pending,
        description="Status da inscrição"
    )
    requested_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp da requisição de inscrição"
    )
    processed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp de processamento (aprovado/rejeitado)"
    )

    # Relacionamento para faixa etária
    age_group: Optional["AgeGroup"] = Relationship(back_populates="enrollments")