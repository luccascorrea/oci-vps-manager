from conf import settings
import oci


class InstanceStatusService:
    """Service to get the status of an instance."""

    def run(self) -> "str":
        instance_id = settings["instance_id"]

        core_client = oci.core.ComputeClient(settings)
        instance = core_client.get_instance(instance_id=instance_id)
        return instance.data.lifecycle_state
