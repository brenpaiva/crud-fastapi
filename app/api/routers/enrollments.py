
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.db.session import get_session
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.age_group import AgeGroup
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentRead, EnrollmentBase
from app.services.enrollment_services import create_enrollment as create_enrollment_service
from app.queue.redis_backend import redis_queue
from app.core.security import get_current_user

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> EnrollmentRead:
    """Cria uma nova inscrição com validação de faixa etária (requer autenticação)."""
    enrollment_created = await create_enrollment_service(enrollment, session)
    await redis_queue.enqueue({"enrollment_id": str(enrollment_created.id)})
    return enrollment_created


@router.get("/", response_model=List[Enrollment])
async def list_enrollments(
    status_filter: Optional[EnrollmentStatus] = None,
    session: AsyncSession = Depends(get_session)
) -> List[Enrollment]:
    """Lista todas as inscrições com filtro opcional por status."""
    stmt = select(Enrollment)
    if status_filter:
        stmt = stmt.where(Enrollment.status == status_filter)
    result = await session.exec(stmt)
    return result.all()


@router.get("/{enrollment_id}", response_model=Enrollment)
async def get_enrollment(
    enrollment_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> Enrollment:
    """Busca uma inscrição específica por ID."""
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@router.patch("/{enrollment_id}/status", response_model=Enrollment)
async def update_enrollment_status(
    enrollment_id: UUID,
    new_status: EnrollmentStatus,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> Enrollment:
    """Atualiza apenas o status de uma inscrição (requer autenticação)."""
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollment.status = new_status
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)
    return enrollment


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> None:
    """Remove uma inscrição (requer autenticação)."""
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    await session.delete(enrollment)
    await session.commit()


@router.put("/{enrollment_id}", response_model=Enrollment)
async def update_enrollment(
    enrollment_id: UUID,
    enrollment_update: EnrollmentBase,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> Enrollment:
    """Atualiza completamente uma inscrição (requer autenticação)."""
    enrollment = await session.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    update_data = enrollment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(enrollment, key, value)
    session.add(enrollment)
    await session.commit()
    await session.refresh(enrollment)
    return enrollment