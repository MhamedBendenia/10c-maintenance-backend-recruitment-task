from core.businesslogic.errors import CannotInvestIntoProjectException
from core.models import Investor, Project


def invest_into_project(investor: Investor, project: Project) -> None:
    """
    Funds project.

    :raises CannotInvestIntoProjectException: If funding criteria were not met.
    """

    if project.funded:
        raise CannotInvestIntoProjectException("Project already funded")

    if investor.remaining_amount < project.amount:
        raise CannotInvestIntoProjectException("Investor has not enough money remaining")

    if investor.individual_amount < project.amount:
        raise CannotInvestIntoProjectException("Investor's individual amount is less than project's amount")

    if investor.project_delivery_deadline < project.delivery_date:
        raise CannotInvestIntoProjectException("Project is not meeting investor's deadline")

    try:
        # Updating project information
        project.funded = True
        project.funded_by = investor
        project.save()

        # Updating investor information
        investor.remaining_amount = investor.remaining_amount - project.amount
        investor.save()
    except Exception as e:
        print(str(e))
