from abc import ABC, abstractmethod,ABCMeta
from typing import Self, List


class AbstractListr(ABC,metaclass=ABCMeta):
    def __init__(
        self,
        task: str,
        parent: Self,
        children: List[Self] | None = None,
        completed: bool = False,
    ) -> None:
        self.task = task
        self.parent = parent
        self.children = children
        self.completed = completed


    @abstractmethod
    def get_child(self) -> Self:
        pass

    @abstractmethod
    def add_child(self, task) -> None:
        pass

    @abstractmethod
    def complete(self, child) -> None:
        pass

    @abstractmethod
    def remove_child(self) -> None:
        pass

    @abstractmethod
    def get_parent(self) -> Self:
        pass
