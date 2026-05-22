from datetime import datetime
from typing import Optional, Type, Union

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def fully_invest(
    target: Type[Union[CharityProject, Donation]]
):
    target.fully_invested = True
    target.close_date = datetime.now()


def check_project_to_close(
        project: CharityProject
):
    if project.full_amount == project.invested_amount:
        fully_invest(project)


def invest(
        sources_projects: list[CharityProject],
        sources_donations: list[Donation],
        target_project: Optional[CharityProject] = None,
        target_donation: Optional[Donation] = None,
):
    sources_donations = sources_donations.scalars().all()
    if target_donation:
        sources_donations.append(target_donation)

    sources_projects = sources_projects.scalars().all()
    if target_project:
        sources_projects.append(target_project)

    changed_projects = []
    changed_donations = []

    for pr in sources_projects:
        money_left_in_project = pr.full_amount - pr.invested_amount
        for don in sources_donations:
            money_left_in_donation = don.full_amount - don.invested_amount
            to_invest = min(money_left_in_project, money_left_in_donation)

            pr.invested_amount += to_invest
            don.invested_amount += to_invest
            if don.invested_amount == don.full_amount:
                fully_invest(don)

            changed_donations.append(don)

        if pr.full_amount == pr.invested_amount:
            fully_invest(pr)
        changed_projects.append(pr)

    return changed_projects, changed_donations
