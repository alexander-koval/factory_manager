from typing import Generic, Protocol, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from .models import Base, Equipment, Factory, Section

M = TypeVar("M", bound=Base, covariant=True)


class Repository(Protocol[M]):
    async def get_by_id(self, item_id: int) -> M | None:
        ...


class HierarchyRepository(Repository[M]):
    async def get_with_relatives(self, item_id: int) -> M | None:
        ...


class BaseRepository(Generic[M]):
    def __init__(self, model: Type[M], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, item_id: int) -> M | None:
        return await self.session.get(self.model, item_id)


class FactoryRepository(BaseRepository[Factory]):
    def __init__(self, session: AsyncSession):
        super().__init__(Factory, session)

    async def get_with_relatives(self, item_id: int) -> Factory | None:
        query = select(self.model).options(
            selectinload(Factory.sections).selectinload(Section.equipment)
        )
        query = query.where(self.model.id == item_id)
        result = await self.session.execute(query)
        return result.scalars().first()


class SectionRepository(BaseRepository[Section]):
    def __init__(self, session: AsyncSession):
        super().__init__(Section, session)

    async def get_with_relatives(self, item_id: int) -> Section | None:
        query = select(self.model).options(
            selectinload(Section.equipment), joinedload(Section.factory)
        )
        query = query.where(self.model.id == item_id)
        result = await self.session.execute(query)
        return result.scalars().first()


class EquipmentRepository(BaseRepository[Equipment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Equipment, session)

    async def get_with_relatives(self, item_id: int) -> Equipment | None:
        query = select(self.model).options(
            selectinload(Equipment.sections).joinedload(Section.factory)
        )
        query = query.where(self.model.id == item_id)
        result = await self.session.execute(query)
        return result.scalars().first()
