
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.session import get_session
from app.models.age_group import AgeGroup
from app.schemas.age_group_schema import AgeGroupUpdate
from app.core.security import get_current_user

router = APIRouter(prefix="/age-groups", tags=["Age Groups"])


@router.post("/", response_model=AgeGroup, status_code=status.HTTP_201_CREATED)
async def create_age_group(
    age_group: AgeGroup,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> AgeGroup:
    """Cria uma nova faixa etária (requer autenticação)."""
    session.add(age_group)
    await session.commit()
    await session.refresh(age_group)
    return age_group


@router.get("/", response_model=List[AgeGroup])
async def list_age_groups(
    session: AsyncSession = Depends(get_session)
) -> List[AgeGroup]:
    """Lista todas as faixas etárias disponíveis."""
    result = await session.exec(select(AgeGroup))
    return result.all()


@router.get("/{age_group_id}", response_model=AgeGroup)
async def get_age_group(
    age_group_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> AgeGroup:
    """Busca uma faixa etária específica por ID."""
    age_group = await session.get(AgeGroup, age_group_id)
    if not age_group:
        raise HTTPException(status_code=404, detail="Age group not found")
    return age_group


@router.delete("/{age_group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_age_group(
    age_group_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> None:
    """Remove uma faixa etária (requer autenticação)."""
    age_group = await session.get(AgeGroup, age_group_id)
    if not age_group:
        raise HTTPException(status_code=404, detail="Age group not found")
    await session.delete(age_group)
    await session.commit()


@router.put("/{age_group_id}", response_model=AgeGroup)
async def update_age_group(
    age_group_id: UUID,
    age_group_update: AgeGroupUpdate,
    session: AsyncSession = Depends(get_session),
    user: str = Depends(get_current_user)
) -> AgeGroup:
    """Atualiza uma faixa etária existente (requer autenticação)."""
    age_group = await session.get(AgeGroup, age_group_id)
    if not age_group:
        raise HTTPException(status_code=404, detail="Age group not found")
    update_data = age_group_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(age_group, key, value)
    session.add(age_group)
    await session.commit()
    await session.refresh(age_group)
    return age_group