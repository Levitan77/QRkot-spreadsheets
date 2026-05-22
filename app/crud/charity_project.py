from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_by_name(
        self,
        name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_project = await self.get_by_attribute('name', name, session)
        if charity_project:
            return charity_project

    async def get_left_projects(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        return await session.execute(
            select(CharityProject).where(
                CharityProject.invested_amount < CharityProject.full_amount
            )
        )

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        projects = (
            select(
                CharityProject,
                (
                    func.strftime("%s", CharityProject.close_date).__sub__(
                        func.strftime("%s", CharityProject.create_date)
                    )
                ).label("time"),
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by("time")
        )
        closed_projects = await session.execute(projects)
        return closed_projects


charity_crud = CRUDCharityProject(CharityProject)
