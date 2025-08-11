from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.age_group import AgeGroup


class EnrollmentStatus(str, Enum):
    """Status possíveis para uma inscrição."""
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Enrollment(SQLModel, table=True):
    """
    Modelo para inscrições de usuários em faixas etárias.
    
    Cada inscrição deve estar vinculada a uma faixa etária válida
    e a idade do inscrito deve estar dentro dos limites da faixa.
    """
    __tablename__ = "enrollments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(..., description="Nome completo do inscrito")
    email: str = Field(..., description="Email de contato")
    age: int = Field(..., ge=0, le=120, description="Idade atual")
    age_group_id: UUID = Field(..., foreign_key="age_groups.id", description="ID da faixa etária")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.pending, description="Status da inscrição")

    age_group: Optional["AgeGroup"] = Relationship(back_populates="enrollments")