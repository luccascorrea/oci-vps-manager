import rumps


class OCIStatusBarApp(rumps.App):
    default_notification_title = "VPS"

    def __init__(self, *args, **kwargs):
        self.instance_status_service = kwargs.pop("instance_status_service")
        self.instance_start_service = kwargs.pop("instance_start_service")
        self.instance_stop_service = kwargs.pop("instance_stop_service")
        self.current_spend_service = kwargs.pop("current_spend_service")

        super().__init__(*args, **kwargs)
        self.menu = ["Start instance", "Stop instance", "View current spend"]

    @rumps.timer(10)
    def update_status(self, _):
        status = self.instance_status_service.run()
        self.title = f"VPS: {status}"

    @rumps.clicked("Start instance")
    def start_instance(self, sender):
        self.instance_start_service.run()
        rumps.notification(
            title=self.default_notification_title,
            subtitle="Instance action",
            message="Started",
        )

    @rumps.clicked("Stop instance")
    def stop_instance(self, _):
        self.instance_stop_service.run()
        rumps.notification(
            title=self.default_notification_title,
            subtitle="Instance action",
            message="Stopped",
        )

    @rumps.clicked("View current spend")
    def view_current_spend(self, _):
        spend: "float" = self.current_spend_service.run()
        rumps.notification(
            title=self.default_notification_title,
            subtitle="Current spend",
            message=f"${spend:.2f}",
        )
