from conf import settings
import oci


class InstanceStopService:
    """Service to stop an instance."""

    def run(self) -> "str":
        instance_id = settings["instance_id"]

        core_client = oci.core.ComputeClient(settings)
        core_client.instance_action(instance_id=instance_id, action="STOP")
