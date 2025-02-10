import rumps
from plugins import load_plugins
from Foundation import NSBundle



class OCIStatusBarApp(rumps.App):
    default_notification_title = "VPS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = []
        self.timers = []

        for plugin in load_plugins(app=self):
            for menu_item in plugin.get_menu_items():
                self.menu.add(menu_item)
                self.timers.extend(plugin.get_timers())
        NSBundle.mainBundle().infoDictionary()['CFBundleIdentifier'] = kwargs["name"]

    def run(self, *args, **kwargs):
        for timer in self.timers:
            timer.start()
        super().run(*args, **kwargs)
