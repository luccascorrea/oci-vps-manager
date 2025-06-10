from plugins.base import BaseCLIPlugin
from .services import InstanceStartService, InstanceStopService, CurrentSpendService, InstanceStatusService



class VPSCLIPlugin(BaseCLIPlugin):
    def get_name(self) -> str:
        return "vps"

    def get_commands(self) -> "List[str]":
        return [
            "start",
            "stop",
            "spend",
            "status",
        ]

    def get_help(self) -> str:
        return (
            "- start: Start the VPS instance\n"
            "- stop: Stop the VPS instance\n"
            "- spend: View current spend on the VPS\n"
            "- status: Get the current status of the VPS instance"
        )

    def run_command(self, command: str, *args, **kwargs) -> str:
        if command == "start":
            service = InstanceStartService()
            service.run()
            return "Instance started successfully."
        elif command == "stop":
            service = InstanceStopService()
            service.run()
            return "Instance stopped successfully."
        elif command == "spend":
            service = CurrentSpendService()
            spend = service.run()
            return f"Current spend: ${spend:.2f}"
        elif command == "status":
            service = InstanceStatusService()
            status = service.run()
            return f"Instance status: {status}"
        else:
            raise ValueError(f"Unknown command: {command}")
