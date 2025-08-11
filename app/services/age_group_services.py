from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from app.models.age_group import AgeGroup
from app.schemas.age_group_schema import AgeGroupCreate, AgeGroupRead


async def create_age_group(
    age_group_in: AgeGroupCreate,
    session: AsyncSession,
) -> AgeGroupRead:
    """
    Cria uma nova faixa etária validando a consistência dos limites de idade.
    
    Args:
        age_group_in: Dados da faixa etária a ser criada
        session: Sessão do banco de dados
        
    Returns:
        AgeGroupRead: Faixa etária criada com ID gerado
        
    Raises:
        HTTPException: Se min_age for maior que max_age
    """
    if age_group_in.min_age > age_group_in.max_age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_age não pode ser maior que max_age",
        )

    new_age_group = AgeGroup(**age_group_in.model_dump())
    session.add(new_age_group)
    await session.commit()
    await session.refresh(new_age_group)
    return AgeGroupRead.model_validate(new_age_group)


async def get_age_groups(
    session: AsyncSession,
) -> List[AgeGroupRead]:
    """
    Retorna todas as faixas etárias cadastradas no sistema.
    
    Args:
        session: Sessão do banco de dados
        
    Returns:
        List[AgeGroupRead]: Lista de todas as faixas etárias
    """
    result = await session.exec(select(AgeGroup))
    age_groups = result.all()
    return [AgeGroupRead.model_validate(ag) for ag in age_groups]


async def delete_age_group(
    age_group_id: int,
    session: AsyncSession,
) -> bool:
    """
    Remove uma faixa etária por ID.
    
    Args:
        age_group_id: ID da faixa etária a ser removida
        session: Sessão do banco de dados
        
    Returns:
        bool: True se removida com sucesso, False se não encontrada
    """
    age_group = await session.get(AgeGroup, age_group_id)
    if not age_group:
        return False
    await session.delete(age_group)
    await session.commit()
    return True