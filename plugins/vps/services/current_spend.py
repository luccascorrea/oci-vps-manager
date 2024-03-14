from conf import settings
import oci


class CurrentSpendService:
    """Service to calculate current spend"""

    def run(self) -> "float":

        config = settings["vps"]["config"]
        compartment_id = config["compartment_id"]
        core_client = oci.budget.BudgetClient(config)
        response = core_client.list_budgets(compartment_id=compartment_id)
        return response.data[0].actual_spend


