from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from loguru import logger
from sqladmin import Admin
from starlette import status

from factory_manager import database
from factory_manager.admin import EquipmentAdmin, FactoryAdmin, SectionAdmin
from factory_manager.bootstrap import create_initial_factories
from factory_manager.schemas import RelativesResponse
from factory_manager.services import HierarchyService
from factory_manager.wiring import get_hierarchy_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup: initializing factories")

    async for session in database.get_async_session():
        try:
            await create_initial_factories(session)
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            raise

    yield

    logger.info("Application shutdown: cleaning up resources")


fhm = FastAPI(
    title="Factory Hierarchy Manager", debug=True, lifespan=lifespan
)

admin = Admin(fhm, engine=database.engine)

admin.add_view(FactoryAdmin)
admin.add_view(SectionAdmin)
admin.add_view(EquipmentAdmin)


@fhm.get(
    "/api/v1/relatives/{model_name}/{item_id}",
    response_model=RelativesResponse,
    tags=["Hierarchy"],
    summary="Get all relatives for a specific item",
)
async def get_relatives_api(
    model_name: str,
    item_id: int,
    service: Annotated[HierarchyService, Depends(get_hierarchy_service)],
):
    relatives_data = await service.get_relatives_for_item(item_id)
    if relatives_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id {item_id} not found in {model_name}"
        )
    return relatives_data
