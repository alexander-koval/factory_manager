from typing import Any, TypedDict

from factory_manager.models import Equipment, Factory, Section
from factory_manager.repositories import HierarchyRepository
from factory_manager.schemas import ModelTypeName, RelativesResponse


class HierarchyLevelDict(TypedDict):
    type: ModelTypeName
    items: list[Any]


def _calculate_relatives(instance: Factory | Section | Equipment) -> dict:
    parents: dict[str, HierarchyLevelDict] = {}
    children: dict[str, HierarchyLevelDict] = {}

    if isinstance(instance, Equipment):
        sections = instance.sections
        if sections:
            parents["0"] = { "type": ModelTypeName.SECTIONS, "items": sections }

        factories = list({s.factory for s in sections})
        if factories:
            parents["1"] = { "type": ModelTypeName.FACTORIES, "items": factories }
    elif isinstance(instance, Section):
        factory = instance.factory
        if factory:
            parents["0"] = { "type": ModelTypeName.FACTORIES, "items": [factory] }

        equipment = instance.equipment
        if equipment:
            children["0"] = { "type": ModelTypeName.EQUIPMENT, "items": equipment }

    elif isinstance(instance, Factory):
        sections = instance.sections
        if sections:
            children["0"] = { "type": ModelTypeName.SECTIONS, "items": sections }

        equipment = list({eq for s in sections for eq in s.equipment})
        if equipment:
            children["1"] = { "type": ModelTypeName.EQUIPMENT, "items": equipment }

    return {"parents": parents, "children": children}


class HierarchyService:
    def __init__(self, repo: HierarchyRepository):
        self.repo = repo

    async def get_relatives_for_item(self, item_id: int) -> RelativesResponse | None:
        instance: (
            Factory | Section | Equipment | None
        ) = await self.repo.get_with_relatives(item_id)
        if not instance:
            return None
        relatives_dict = _calculate_relatives(instance)
        return RelativesResponse.model_validate(relatives_dict)
