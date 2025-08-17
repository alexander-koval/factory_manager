from enum import StrEnum
from typing import List, Union

from pydantic import BaseModel, ConfigDict


class BaseItem(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class EquipmentRead(BaseItem):
    pass


class SectionRead(BaseItem):
    pass


class FactoryRead(BaseItem):
    pass


class ModelTypeName(StrEnum):
    FACTORIES = "factories"
    SECTIONS = "sections"
    EQUIPMENT = "equipment"


class HierarchyLevel(BaseModel):
    type: ModelTypeName
    items: List[Union[FactoryRead, SectionRead, EquipmentRead]]


class RelativesResponse(BaseModel):
    parents: dict[str, HierarchyLevel]
    children: dict[str, HierarchyLevel]
