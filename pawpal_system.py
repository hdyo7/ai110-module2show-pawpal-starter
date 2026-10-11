"""Dataclass-based skeleton matching diagrams/uml_draft.mmd."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class task:
    description: str
    time: datetime
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class pet:
    name: str
    species: str
    tasks: list[task] = field(default_factory=list)


@dataclass
class owner:
    name: str
    pets: list[pet] = field(default_factory=list)

    def get_all_tasks(self) -> list[task]:
        pass


class scheduler:
    def create_schedule(self, owner: owner) -> list[task]:
        pass