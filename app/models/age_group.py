from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.enrollment import Enrollment

class AgeGroup(SQLModel, table=True):
    __tablename__ = "age_groups"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(..., description="Nome da faixa etária, ex: 'Sub-10', 'Adulto'")
    min_age: int = Field(..., ge=0, description="Idade mínima inclusiva")
    max_age: int = Field(..., ge=0, description="Idade máxima inclusiva")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Data de criação")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Data da última atualização")

    # Relacionamento inverso para inscrições
    enrollments: List["Enrollment"] = Relationship(back_populates="age_group")