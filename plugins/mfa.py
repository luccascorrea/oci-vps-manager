from typing import Dict, List, TypedDict
from plugins.base import BasePlugin
from conf import settings
from utils import copy_to_clipboard
import uuid
import pyotp
import rumps

OTP_INTERVAL = 30

class MFASettings(TypedDict):
    secret: str
    label: str
    interval: int

def generate_otp(secret: str, interval: int):
    totp = pyotp.TOTP(secret, interval=interval)
    return totp.now()

class MFAPlugin(BasePlugin):
    mfa_settings_map: Dict[str, MFASettings]

    def __init__(self):
        self.mfa_settings_map = {}
        mfa_settings_list: List[MFASettings] = settings.get("mfa", [])
        for mfa_settings in mfa_settings_list:
            identifier = uuid.uuid4().hex
            self.mfa_settings_map[identifier] = mfa_settings


    def get_menu_items(self) -> List[rumps.MenuItem]:
        items = []
        for identifier, mfa_settings in self.mfa_settings_map.items():
            menu_item = rumps.MenuItem(
                title=mfa_settings["label"],
                callback=self.on_click,
                key=identifier,
            )
            items.append(menu_item)

        if items:
            parent_item = rumps.MenuItem(title="MFA")
            for item in items:
                parent_item.add(item)
            return [parent_item]

        return []
 
    def on_click(self, item):
        identifier = item.key
        mfa_settings = self.mfa_settings_map[identifier]
        otp = generate_otp(secret=mfa_settings["secret"], interval=mfa_settings["interval"])
        copy_to_clipboard(otp)
        rumps.notification(
            title="MFA",
            subtitle="Copied!",
            message=f"{otp}",
        )


