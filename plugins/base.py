from abc import ABC, abstractmethod
from typing import List

from rumps import MenuItem, Timer


class BasePlugin(ABC):
    @abstractmethod
    def get_menu_items(self) -> "List[MenuItem]":
        pass

    def get_timers(self) -> "List[Timer]":
        return []
