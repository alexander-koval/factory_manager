from sqladmin import ModelView

from factory_manager.models import Equipment, Factory, Section


class FactoryAdmin(ModelView, model=Factory):
    name_plural = "Factories"
    column_list = [Factory.id, Factory.name, Factory.sections]


class SectionAdmin(ModelView, model=Section):
    column_list = [Section.id, Section.name, Section.equipment]


class EquipmentAdmin(ModelView, model=Equipment):
    column_list = [Equipment.id, Equipment.name]
