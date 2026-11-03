from typing import List
from plugins.base import BaseCLIPlugin
from .services import UpdateRulesService, FetchCIDRsService, get_external_ip


class IPSecurityCLIPlugin(BaseCLIPlugin):
    def get_name(self) -> str:
        return "ip"

    def get_commands(self) -> List[str]:
        return [
            "update",
            "current",
            "list",
        ]

    def get_help(self) -> str:
        return (
            "- update [ip]: Update security rules to allow IP (defaults to current external IP)\n"
            "- current: Get current external IP address\n"
            "- list: List currently configured CIDRs across providers"
        )

    def run_command(self, command: str, *args, **kwargs) -> str:
        if command == "update":
            if args:
                ip = args[0].strip()
                if ip.endswith("/32"):
                    ip = ip[:-3]
            else:
                ip = get_external_ip()

            service = UpdateRulesService()
            service.run(ip)
            return f"Security rules successfully updated to allow {ip} ({ip}/32)."
        elif command == "current":
            ip = get_external_ip()
            return f"Current external IP: {ip}"
        elif command == "list":
            service = FetchCIDRsService()
            cidrs_info = service.run()
            lines = []
            for info in cidrs_info:
                provider = info["provider"].upper()
                for cidr in info["cidrs"]:
                    lines.append(f"[{provider}] {cidr['current_cidr']} ({cidr['description']})")
            if not lines:
                return "No CIDRs configured or found."
            return "\n".join(lines)
        else:
            raise ValueError(f"Unknown command: {command}")
