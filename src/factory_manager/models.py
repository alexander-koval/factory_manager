from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


section_equipment_association = Table(
    "section_equipment_association",
    Base.metadata,
    Column("section_id", Integer, ForeignKey("sections.id"), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.id"), primary_key=True),
)


class Factory(Base):
    __tablename__ = "factories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    sections: Mapped[List["Section"]] = relationship(
        back_populates="factory", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Factory(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return f"{self.name}"


class Section(Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    factory_id: Mapped[int] = mapped_column(ForeignKey("factories.id"))

    factory: Mapped["Factory"] = relationship(back_populates="sections")

    equipment: Mapped[List["Equipment"]] = relationship(
        secondary=section_equipment_association, back_populates="sections"
    )

    def __repr__(self) -> str:
        return f"<Section(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return f"{self.name}"


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    sections: Mapped[List["Section"]] = relationship(
        secondary=section_equipment_association, back_populates="equipment"
    )

    def __repr__(self) -> str:
        return f"<Equipment(id={self.id}, name='{self.name}')>"

    def __str__(self) -> str:
        return f"{self.name}"
