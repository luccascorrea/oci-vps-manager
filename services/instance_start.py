from conf import settings
import oci


class InstanceStartService:
    """Service to start an instance."""

    def run(self) -> "str":
        instance_id = settings["instance_id"]

        core_client = oci.core.ComputeClient(settings)
        core_client.instance_action(instance_id=instance_id, action="START")
