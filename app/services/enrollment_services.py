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
    Cria uma nova inscrição validando a faixa etária e a idade do inscrito.
    
    Args:
        enrollment_in: Dados da inscrição a ser criada
        session: Sessão do banco de dados
        
    Returns:
        EnrollmentRead: Inscrição criada com status pendente
        
    Raises:
        HTTPException: Se a faixa etária não existir ou idade for inválida
    """
    age_group = await session.get(AgeGroup, enrollment_in.age_group_id)
    if not age_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AgeGroup não encontrado",
        )
    if not (age_group.min_age <= enrollment_in.age <= age_group.max_age):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Idade deve estar entre {age_group.min_age} e {age_group.max_age}",
        )

    new_enrollment = Enrollment(**enrollment_in.model_dump())
    session.add(new_enrollment)
    await session.commit()
    await session.refresh(new_enrollment)
    return EnrollmentRead.model_validate(new_enrollment)


async def get_enrollment(
    enrollment_id: int,
    session: AsyncSession,
) -> EnrollmentRead | None:
    """
    Busca uma inscrição por ID.
    
    Args:
        enrollment_id: ID da inscrição
        session: Sessão do banco de dados
        
    Returns:
        EnrollmentRead | None: Inscrição encontrada ou None se não existir
    """
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        return None
    return EnrollmentRead.model_validate(enrollment)