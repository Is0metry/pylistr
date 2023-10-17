from abc import ABCMeta
from typing import List, Optional, Self

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import DeclarativeMeta

from .listr import AbstractListr


class CombinedMeta(DeclarativeMeta, ABCMeta):
    pass


Base = orm.declarative_base(metaclass=CombinedMeta)


class SQListr(Base, AbstractListr):
    __tablename__ = "listr"
    id = sa.Column(sa.Integer, primary_key=True)
    task = sa.Column(sa.String)
    completed = sa.Column(sa.Boolean, default=False)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("listr.id"))

    parent = orm.relationship("SQListr", remote_side=[id], back_populates="children")
    children = orm.relationship("SQListr", back_populates="parent")

    def __init__(
        self,
        task: str,
        parent: Optional["SQListr"] = None,
        children: Optional[List["SQListr"]] = None,
        completed: bool = False,
    ) -> None:
        if parent is None:
            parent = self
        if children is None:
            children = []
        super().__init__(task=task, parent=parent, children=children)

    def __str__(self) -> str:
        task_str = f"{self.task}  {'✅' if self.completed else ''}"
        task_str += "\n    " + "\n    ".join(
            [
                f"{i+1}. {child.task} {'✅' if self.completed else ''}"
                for i, child in enumerate(self.children)
                if child.id != self.id
            ]
        )
        return task_str

    def get_child(self, child: int) -> Self | None:
        return self.children[child] if self.children else None

    def add_child(self, task: str) -> None:
        child = SQListr(task, self)
        self.children.append(child)

    def complete(self) -> None:
        self.completed = True
        for child in self.children:
            child.complete()

    def remove_child(self, child: int) -> None:
        if 0 <= child < len(self.children):
            self.children.pop(child)

    def get_parent(self) -> Self:
        return self.parent
