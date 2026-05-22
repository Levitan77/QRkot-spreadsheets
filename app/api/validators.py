from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_crud
from app.models.charity_project import CharityProject


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_crud.get_project_by_name(name, session)
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_is_open(
        project: CharityProject
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект закрыт!'
        )


async def check_project_is_invested(
        project: CharityProject
) -> None:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже инвестировали!'
        )


async def check_bad_editing(
        project: CharityProject,
        new_project: CharityProject,
) -> None:
    if (
        new_project.full_amount and
        project.invested_amount > new_project.full_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Это поменять нельзя!'
        )
