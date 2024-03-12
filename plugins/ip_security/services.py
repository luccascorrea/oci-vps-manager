from typing import TypedDict
import requests
from requests.adapters import HTTPAdapter, Retry
from conf import settings
from plugins.ip_security.backends import get_backend
from plugins.ip_security.backends.base import CurrentCidr


def get_external_ip() -> str:
    session = requests.Session()
    retry = Retry(total=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    response = session.get("https://api.ipify.org")
    return response.text


class BackendSettings(TypedDict):
    auth: dict
    rules_info: dict
    provider: str


class UpdateRulesService:
    def run(self, new_ip: str):
        new_cidr = f"{new_ip}/32"
        all_backend_settings: list[BackendSettings] = settings.get("ip_security", [])

        for backend_settings in all_backend_settings:
            auth = backend_settings["auth"]
            provider = backend_settings["provider"]
            backend = get_backend(
                provider=provider,
                auth=auth,
            )
            rules_info = backend_settings["rules_info"]
            backend.update_rules(rules_info, new_cidr)


class CurrentCIDRsInfo(TypedDict):
    provider: str
    cidrs: list[CurrentCidr]


class FetchCIDRsService:
    def run(self) -> list[CurrentCIDRsInfo]:
        all_backend_settings: list[BackendSettings] = settings.get("ip_security", [])
        cidrs = []
        for backend_settings in all_backend_settings:
            auth = backend_settings["auth"]
            provider = backend_settings["provider"]
            backend = get_backend(
                provider=provider,
                auth=auth,
            )
            rules_info = backend_settings["rules_info"]
            cidrs.append(
                {
                    "provider": provider,
                    "cidrs": backend.get_current_cidrs(rules_info),
                }
            )
        return cidrs


class CheckNeedUpdateService:
    def run(self, cidrs: list[CurrentCIDRsInfo], current_external_ip: str) -> bool:
        different = False
        current_external_ip = current_external_ip + "/32"
        for cidr_info in cidrs:
            for cidr in cidr_info["cidrs"]:
                if cidr["current_cidr"] != current_external_ip:
                    different = True
                    break
        return different
