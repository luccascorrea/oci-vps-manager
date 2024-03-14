from typing import List
from rumps import MenuItem, Timer, notification
from plugins.base import BasePlugin
from .services import (
    CurrentCIDRsInfo,
    UpdateRulesService,
    CheckNeedUpdateService,
    FetchCIDRsService,
    get_external_ip,
)


class IPSecurityPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        self.root_item = MenuItem("IP Security")
        self.update_cidrs_menu_item = MenuItem(
            "Update CIDRs", key="update_cidrs", callback=self.update_rules_cidrs
        )
        self.current_external_ip = None
        self.cidrs: "List[CurrentCIDRsInfo]" = []
        self.auto_update = True

    def get_menu_items(self) -> "list[MenuItem]":
        self.root_item.add(self.update_cidrs_menu_item)
        return [self.root_item]

    def get_timers(self) -> "list[Timer]":
        return [Timer(self.update_external_ip, 60), Timer(self.fetch_cidrs, 600)]

    def update_external_ip(self, _):
        try:
            new_external_ip = get_external_ip()
            ip_changed = new_external_ip != self.current_external_ip
            if ip_changed:
                self.current_external_ip = new_external_ip
                self.update_external_ip_text()

        except Exception:
            pass

    def update_external_ip_text(self):

        # Check if the current external IP is in the CIDRs
        text = f"Update CIDRs ({self.current_external_ip})"
        if self.cidrs and self.current_external_ip:
            service = CheckNeedUpdateService()
            need_update = service.run(self.cidrs, self.current_external_ip)
            if need_update:
                text += " *"

                if self.auto_update:
                    self.update_rules_cidrs(None)

        self.update_cidrs_menu_item.title = text

    def update_rules_cidrs(self, _):
        if not self.current_external_ip:
            return
        service = UpdateRulesService()
        service.run(self.current_external_ip)
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

        self.cidrs = cidrs
        for cidr_info in cidrs:
            provider = cidr_info["provider"]
            cidrs = cidr_info["cidrs"]
            for cidr in cidrs:
                text = f"{provider}: {cidr['current_cidr']} ({cidr['description']})"
                cidr_item = MenuItem(text)
                self.root_item.add(cidr_item)

        self.update_external_ip_text()
