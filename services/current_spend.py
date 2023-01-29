from conf import settings
import oci


class CurrentSpendService:
    """Service to calculate current spend"""

    def run(self) -> "float":
        compartment_id = settings["compartment_id"]

        core_client = oci.budget.BudgetClient(settings)
        response = core_client.list_budgets(compartment_id=compartment_id)
        return response.data[0].actual_spend


