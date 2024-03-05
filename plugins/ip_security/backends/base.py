from abc import ABC, abstractmethod
from typing import TypedDict


class UnknownProviderError(Exception):
    pass


class CurrentCidr(TypedDict):
    current_cidr: str
    description: str


class IPRulesBackend(ABC):
    @abstractmethod
    def update_rules(self, rules_info: "dict", new_cidr: str):
        pass

    @abstractmethod
    def get_current_cidrs(self, rules_info: "dict") -> list[CurrentCidr]:
        pass


def get_backend(provider: str, auth: dict) -> IPRulesBackend:
    if provider== "aws":
        from plugins.ip_security.backends.aws import AWSBackend

        return AWSBackend(auth)
    else:
        raise UnknownProviderError(f"Provider type {provider} not available")
