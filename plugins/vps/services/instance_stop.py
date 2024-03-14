from conf import settings
import oci


class InstanceStopService:
    """Service to stop an instance."""

    def run(self) -> "str":
        config = settings["vps"]["config"]
        instance_id = config["instance_id"]

        core_client = oci.core.ComputeClient(config)
        core_client.instance_action(instance_id=instance_id, action="STOP")
