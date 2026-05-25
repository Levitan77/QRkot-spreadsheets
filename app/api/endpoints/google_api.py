from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.services.google_api import (create_spreadsheets, set_user_permissions,
                                     update_spreadsheets_value)

google_router = APIRouter()


@google_router.post(
    '/',
    response_model=list[dict[str, int]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    closed_projects = await charity_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheet_id, spreadsheet_url = await create_spreadsheets(
        wrapper_services
    )
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await update_spreadsheets_value(
            spreadsheet_id,
            closed_projects,
            wrapper_services
        )

        return {'url': spreadsheet_url}
    except TypeError as error:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при попытке обновления данных: {error}'
        )
