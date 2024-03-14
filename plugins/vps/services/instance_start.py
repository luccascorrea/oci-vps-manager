from conf import settings
import oci


class InstanceStartService:
    """Service to start an instance."""

    def run(self):
        config = settings["vps"]["config"]
        instance_id = config["instance_id"]

        core_client = oci.core.ComputeClient(config)
        core_client.instance_action(instance_id=instance_id, action="START")
