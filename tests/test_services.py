import pytest

from factory_manager.models import Factory
from factory_manager.schemas import RelativesResponse
from factory_manager.services import HierarchyService
from tests.conftest import MockHierarchyRepository


@pytest.mark.asyncio
async def test_get_relatives_for_factory(
        fully_linked_factory: Factory, mock_repo: MockHierarchyRepository
):
    mock_repo.set_return_value(fully_linked_factory)
    service = HierarchyService(repo=mock_repo)

    result = await service.get_relatives_for_item(item_id=100)

    assert result is not None
    assert isinstance(result, RelativesResponse)

    assert not result.parents

    level0_children = result.children["0"]
    assert level0_children.type == "sections"

    level1_children = result.children["1"]
    assert level1_children.type == "equipment"
    assert len(level1_children.items) == 3


@pytest.mark.asyncio
async def test_get_relatives_for_section(
        fully_linked_factory: Factory, mock_repo: MockHierarchyRepository
):
    section_to_test = fully_linked_factory.sections[0]
    mock_repo.set_return_value(section_to_test)
    service = HierarchyService(repo=mock_repo)

    result = await service.get_relatives_for_item(item_id=10)

    assert result is not None
    level0_parent = result.parents["0"]
    assert level0_parent.type == "factories"

    level0_children = result.children["0"]
    assert level0_children.type == "equipment"


@pytest.mark.asyncio
async def test_item_not_found(mock_repo: MockHierarchyRepository):
    mock_repo.set_return_value(None)
    service = HierarchyService(repo=mock_repo)

    result = await service.get_relatives_for_item(item_id=999)

    assert result is None