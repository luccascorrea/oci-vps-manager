from rumps import MenuItem, Timer, notification
from plugins.base import BasePlugin
from .services import UpdateRulesService, get_external_ip, FetchCIDRsService


class IPSecurityPlugin(BasePlugin):
    def __init__(self):
        self.root_item = MenuItem("IP Security")
        self.update_cidrs_menu_item = MenuItem("Update CIDRs", key="update_cidrs", callback=self.update_rules_cidrs)

    def get_menu_items(self) -> "list[MenuItem]":
        self.root_item.add(self.update_cidrs_menu_item)
        return [self.root_item]

    def get_timers(self) -> "list[Timer]":
        return [Timer(self.update_external_ip, 60), Timer(self.fetch_cidrs, 600)]

    def update_external_ip(self, _):
        try:
            external_ip = get_external_ip()
            self.update_cidrs_menu_item.title = f"Update CIDRs ({external_ip})"
        except Exception:
            self.update_cidrs_menu_item.title = "Update CIDRs (Error)"

    def update_rules_cidrs(self, _):
        service = UpdateRulesService()
        external_ip = get_external_ip()
        service.run(external_ip)
        self.fetch_cidrs(None)

        notification(
            title="IP Security",
            subtitle="Updated!",
            message="Rules and CIDRs updated",
        )

    def fetch_cidrs(self, _):
        service = FetchCIDRsService()
        cidrs = service.run()

        for key, menu_item in self.root_item.items():
            if menu_item is self.update_cidrs_menu_item:
                continue
            self.root_item.pop(key)

        for cidr_info in cidrs:
            provider = cidr_info["provider"]
            cidrs = cidr_info["cidrs"]
            for cidr in cidrs:
                text = f"{provider}: {cidr['current_cidr']} ({cidr['description']})"
                cidr_item = MenuItem(text)
                self.root_item.add(cidr_item)
