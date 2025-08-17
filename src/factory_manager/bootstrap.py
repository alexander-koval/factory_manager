from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from factory_manager.models import Equipment, Factory, Section


async def create_initial_factories(session: AsyncSession):
    result = await session.execute(select(Factory))
    if result.scalars().first() is not None:
        logger.info("Factories exists. Skip creating.")
        return

    logger.info("Creating Factories...")

    eq1 = Equipment(name="Оборудование 1")
    eq2 = Equipment(name="Оборудование 2")
    eq3 = Equipment(name="Оборудование 3")

    section1 = Section(name="Участок 1")
    section1.equipment.extend([eq1, eq2, eq3])

    section2 = Section(name="Участок 2")
    section2.equipment.extend([eq1, eq2])

    factory1 = Factory(name="Фабрика 1")
    factory1.sections.extend([section1, section2])

    session.add(factory1)

    await session.commit()
    logger.info("Factories Created...")
