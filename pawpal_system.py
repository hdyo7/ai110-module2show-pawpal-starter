"""Dataclass-based pet care model matching diagrams/uml_draft.mmd."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time


@dataclass
class task:
    description: str
    frequency: str
    duration_minutes: int
    pet: pet = field(repr=False, compare=False)
    preferred_time: time | None = None
    completed_occurrences: list[datetime] = field(default_factory=list)

    def mark_complete(self, occurrence: datetime) -> None:
        if occurrence not in self.completed_occurrences:
            self.completed_occurrences.append(occurrence)


@dataclass
class pet:
    name: str
    species: str
    tasks: list[task] = field(default_factory=list)

    def add_task(self, new_task: task) -> None:
        new_task.pet = self
        self.tasks.append(new_task)


@dataclass
class owner:
    name: str
    pets: list[pet] = field(default_factory=list)

    def get_all_tasks(self) -> list[task]:
        return [pet_task for pet in self.pets for pet_task in pet.tasks]


class scheduler:
    def create_schedule(self, owner: owner) -> list[task]:
        pass