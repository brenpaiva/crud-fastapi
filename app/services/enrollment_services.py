from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.enrollment import Enrollment
from app.models.age_group import AgeGroup
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentRead


async def create_enrollment(
    enrollment_in: EnrollmentCreate,
    session: AsyncSession,
) -> EnrollmentRead:
    """
    Cria um novo Enrollment, valida faixa etária e retorna o registro pendente.
    """
    # Verifica se AgeGroup existe
    age_group = await session.get(AgeGroup, enrollment_in.age_group_id)
    if not age_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AgeGroup não encontrado",
        )
    # Valida idade dentro da faixa
    if not (age_group.min_age <= enrollment_in.age <= age_group.max_age):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Idade deve estar entre {age_group.min_age} e {age_group.max_age}",
        )

    new_enrollment = Enrollment(**enrollment_in.dict())
    session.add(new_enrollment)
    await session.commit()
    await session.refresh(new_enrollment)
    return EnrollmentRead.from_orm(new_enrollment)


async def get_enrollment(
    enrollment_id: int,
    session: AsyncSession,
) -> EnrollmentRead | None:
    """
    Retorna um Enrollment por ID ou None se não existir.
    """
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        return None
    return EnrollmentRead.from_orm(enrollment)