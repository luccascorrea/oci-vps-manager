from typing import List
from rumps import MenuItem, notification, Timer
from plugins.base import BasePlugin
from .services import (
    InstanceStartService,
    InstanceStopService,
    CurrentSpendService,
    InstanceStatusService,
)


class VPSPlugin(BasePlugin):
    def __init__(self, *args, **kwargs):
        self.instance_start_service = kwargs.pop("instance_start_service", InstanceStartService())
        self.instance_stop_service = kwargs.pop("instance_stop_service", InstanceStopService())
        self.current_spend_service = kwargs.pop("current_spend_service", CurrentSpendService())
        self.instance_status_service = kwargs.pop("instance_status_service", InstanceStatusService())
        self.default_notification_title = "VPS"
        self.app = kwargs.pop("app")

    def get_menu_items(self) -> "List[MenuItem]":

        return [
            MenuItem("Start instance", callback=self.start_instance),
            MenuItem("Stop instance", callback=self.stop_instance),
            MenuItem("View current spend", callback=self.view_current_spend),
        ]

    def get_timers(self) -> "List[Timer]":
        return [
            Timer(self.update_status, 10),
        ]

    def start_instance(self, _):
        self.instance_start_service.run()
        notification(
            title=self.default_notification_title,
            subtitle="Instance action",
            message="Started",
        )

    def stop_instance(self, _):
        self.instance_stop_service.run()
        notification(
            title=self.default_notification_title,
            subtitle="Instance action",
            message="Stopped",
        )

    def view_current_spend(self, _):
        spend: "float" = self.current_spend_service.run()
        notification(
            title=self.default_notification_title,
            subtitle="Current spend",
            message=f"${spend:.2f}",
        )

    def update_status(self, _):
        status = self.instance_status_service.run()
        self.app.title = f"VPS: {status}"
