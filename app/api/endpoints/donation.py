from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investing import invest

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

donation_router = APIRouter()


@donation_router.get(
    '/',
    response_model=List[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(session: SessionDep):
    """
    Получает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@donation_router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
):
    """
    Создает новое пожертвование.
    """
    new_donation = await donation_crud.create(
        donation,
        session,
        to_be_committed=False,
        invested_amount=0,
        user=user
    )
    sources_projects = await charity_crud.get_left_projects(session)
    sources_donations = await donation_crud.get_left_donations(session)
    changed_projects, changed_donations = invest(
        sources_projects, sources_donations, target_donation=new_donation
    )
    session.add_all(changed_projects)
    session.add_all(changed_donations)
    session.add(new_donation)
    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@donation_router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)]
)
async def get_user_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)]
):
    """
    Получает список пожертвований пользователя.
    """
    user_donations = await donation_crud.get_user_donations(session, user)
    return user_donations