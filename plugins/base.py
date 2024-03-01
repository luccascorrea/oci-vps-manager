from abc import ABC, abstractmethod
from typing import List

from rumps import MenuItem


class BasePlugin(ABC):
    @abstractmethod
    def get_menu_items(self) -> "List[MenuItem]":
        pass
