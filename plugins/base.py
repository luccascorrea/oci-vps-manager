from abc import ABC, abstractmethod
from typing import List

from rumps import MenuItem, Timer


class BasePlugin(ABC):
    @abstractmethod
    def get_menu_items(self) -> "List[MenuItem]":
        pass

    def get_timers(self) -> "List[Timer]":
        return []

class BaseCLIPlugin(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_commands(self) -> "List[str]":
        pass

    @abstractmethod
    def get_help(self) -> str:
        pass

    @abstractmethod
    def run_command(self, command: str, *args, **kwargs) -> str:
        pass
