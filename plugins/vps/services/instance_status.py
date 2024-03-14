from conf import settings
import oci


class InstanceStatusService:
    """Service to get the status of an instance."""

    def run(self) -> "str":
        config = settings["vps"]["config"]
        instance_id = config["instance_id"]

        core_client = oci.core.ComputeClient(config)
        instance = core_client.get_instance(instance_id=instance_id)
        return instance.data.lifecycle_state
