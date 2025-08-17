import pytest
from typing import Any

from factory_manager.models import Equipment, Factory, Section
from factory_manager.repositories import HierarchyRepository


class MockHierarchyRepository(HierarchyRepository):
    def __init__(self, return_value: Any = None):
        self._return_value = return_value

    def set_return_value(self, value: Any):
        self._return_value = value

    async def get_by_id(self, item_id: int):
        return None

    async def get_with_relatives(self, item_id: int):
        return self._return_value


@pytest.fixture(scope="session")
def fully_linked_factory() -> Factory:
    eq1 = Equipment(id=1, name="Оборудование 1")
    eq2 = Equipment(id=2, name="Оборудование 2")
    eq3 = Equipment(id=3, name="Оборудование 3")

    section1 = Section(id=10, name="Участок 1")
    section1.equipment = [eq1, eq2]

    section2 = Section(id=20, name="Участок 2")
    section2.equipment = [eq2, eq3]

    factory = Factory(id=100, name="Фабрика 1")
    factory.sections = [section1, section2]

    section1.factory = factory
    section2.factory = factory

    eq1.sections = [section1]
    eq2.sections = [section1, section2]
    eq3.sections = [section2]

    return factory


@pytest.fixture
def mock_repo() -> MockHierarchyRepository:
    return MockHierarchyRepository()