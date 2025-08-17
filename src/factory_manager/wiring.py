from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from factory_manager.database import get_async_session
from factory_manager.repositories import (
    BaseRepository,
    EquipmentRepository,
    FactoryRepository,
    HierarchyRepository,
    SectionRepository,
)
from factory_manager.schemas import ModelTypeName
from factory_manager.services import HierarchyService

REPOSITORY_MAP = {
    ModelTypeName.FACTORIES: FactoryRepository,
    ModelTypeName.SECTIONS: SectionRepository,
    ModelTypeName.EQUIPMENT: EquipmentRepository,
}

def get_repository_factory(
    model_name: str, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> BaseRepository:
    try:
        repo_clazz = REPOSITORY_MAP[ModelTypeName(model_name.lower())]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown model type: '{model_name}'. "
                   f"Available types: {[e.value for e in ModelTypeName]}"
        ) from e
    return repo_clazz(session=session)


def get_hierarchy_service(
    repo: Annotated[HierarchyRepository, Depends(get_repository_factory)],
) -> HierarchyService:
    return HierarchyService(repo=repo)
