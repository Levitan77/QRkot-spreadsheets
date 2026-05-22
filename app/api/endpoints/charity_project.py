from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_bad_editing, check_project_exists,
                                check_project_is_invested,
                                check_project_is_open,
                                check_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import check_project_to_close, invest

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

charity_router = APIRouter()


@charity_router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(session: SessionDep):
    """
    Возвращает список всех благотворительных проектов.
    """
    return await charity_crud.get_multi(session)


@charity_router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: SessionDep,
):
    """
    Создает новый благотворительный проект.
    """
    await check_project_name_duplicate(project.name, session)
    new_project = await charity_crud.create(
        project,
        session,
        to_be_committed=False,
        invested_amount=0
    )
    sources_projects = await charity_crud.get_left_projects(session)
    sources_donations = await donation_crud.get_left_donations(session)
    changed_projects, changed_donations = invest(
        sources_projects, sources_donations, target_project=new_project
    )
    session.add_all(changed_projects)
    session.add_all(changed_donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@charity_router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep
):
    """
    Удаляет информацию по конкретному благотворительному проекту.
    - **project_id**: id благотворительного проекта
    """
    project = await check_project_exists(project_id, session)
    await check_project_is_invested(project)
    removed_project = await charity_crud.remove(project, session)
    return removed_project


@charity_router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    new_project: CharityProjectUpdate,
    session: SessionDep
):
    """
    Изменяет информацию по конкретному благотворительному проекту.
    - **project_id**: id благотворительного проекта
    """
    if new_project.name is not None:
        await check_project_name_duplicate(new_project.name, session)

    project = await check_project_exists(project_id, session)
    await check_project_is_open(project)
    await check_bad_editing(
        project,
        new_project
    )
    updated_project = await charity_crud.update(
        project, new_project, session,
    )
    check_project_to_close(project)
    return updated_project
