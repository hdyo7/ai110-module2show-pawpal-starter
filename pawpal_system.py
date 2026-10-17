"""Dataclass-based pet care model for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta


@dataclass
class Task:
    description: str
    frequency: str
    duration_minutes: int
    pet: Pet | None = field(default=None, repr=False, compare=False)
    preferred_time: time | None = None
    completed_occurrences: list[datetime] = field(default_factory=list)
    due_at: datetime | None = None

    def mark_complete(self, occurrence: datetime) -> Task | None:
        """Record a completion and create the next recurring task when applicable.

        Daily and weekly tasks get a new instance due one or seven days after
        ``occurrence``, respectively. The new task keeps the preferred time, or
        uses the occurrence's time when no preferred time is set. If this task
        belongs to a pet, the new instance is attached to that pet.

        Args:
            occurrence: The date and time this task occurrence was completed.

        Returns:
            The next task for daily or weekly frequencies, or ``None`` if this
            occurrence was already recorded or the frequency is not supported.
        """
        if occurrence in self.completed_occurrences:
            return None
        self.completed_occurrences.append(occurrence)

        days_until_next = {"daily": 1, "weekly": 7}.get(self.frequency.casefold())
        if days_until_next is None:
            return None

        completion_date = occurrence.date()
        next_due_date = completion_date + timedelta(days=days_until_next)
        next_time = self.preferred_time or occurrence.timetz().replace(tzinfo=None)
        next_task = Task(
            description=self.description,
            frequency=self.frequency,
            duration_minutes=self.duration_minutes,
            preferred_time=self.preferred_time,
            due_at=datetime.combine(next_due_date, next_time, tzinfo=occurrence.tzinfo),
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, new_task: Task) -> None:
        """Attach a task to this pet, preventing duplicates and reassignment."""
        if new_task.pet is not None and new_task.pet is not self:
            raise ValueError("A task cannot belong to more than one pet.")
        new_task.pet = self
        if not any(existing_task is new_task for existing_task in self.tasks):
            self.tasks.append(new_task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, new_pet: Pet) -> None:
        """Add a pet to this owner unless it is already present."""
        if not any(existing_pet is new_pet for existing_pet in self.pets):
            self.pets.append(new_pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [pet_task for pet in self.pets for pet_task in pet.tasks]


class Scheduler:
    def detect_time_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Find distinct task pairs with exactly matching preferred times.

        Tasks without a preferred time are ignored. This checks matching start
        times only; it does not compare task durations for overlapping intervals.
        """
        return [
            (task, other_task)
            for index, task in enumerate(tasks)
            if task.preferred_time is not None
            for other_task in tasks[index + 1 :]
            if other_task is not task
            and other_task.preferred_time == task.preferred_time
        ]

    def conflict_warnings(self, tasks: list[Task]) -> list[str]:
        """Format a warning for each pair with the same preferred time.

        Returns an empty list when no task pairs conflict.
        """
        warnings = []
        for first_task, second_task in self.detect_time_conflicts(tasks):
            scheduled_time = first_task.preferred_time
            if scheduled_time is None:
                continue
            warnings.append(
                f"Scheduling conflict at {scheduled_time.strftime('%H:%M')}: "
                f"'{first_task.description}' and '{second_task.description}' "
                "are set for the same time."
            )
        return warnings

    def filter_tasks(
        self,
        tasks: list[Task],
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter by recorded completion history and/or the assigned pet's name.

        A task is considered completed if it has at least one recorded occurrence.
        When both filters are supplied, a task must match both. Pet-name matching
        is case-insensitive; tasks without an assigned pet do not match a name.

        Args:
            tasks: Tasks to filter; the input list is not modified.
            completed: Select completed tasks (``True``), incomplete tasks
                (``False``), or skip status filtering (``None``).
            pet_name: Select tasks assigned to this pet, or skip pet filtering
                when ``None``.

        Returns:
            A new list containing tasks that match all requested filters.
        """
        filtered_tasks = tasks
        if completed is not None:
            filtered_tasks = [
                task
                for task in filtered_tasks
                if bool(task.completed_occurrences) is completed
            ]
        if pet_name is not None:
            normalized_pet_name = pet_name.casefold()
            filtered_tasks = [
                task
                for task in filtered_tasks
                if task.pet is not None
                and task.pet.name.casefold() == normalized_pet_name
            ]
        return filtered_tasks

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by preferred time, placing untimed tasks last.

        The input list is not modified; tasks sharing a time retain their
        original relative order.
        """
        return sorted(
            tasks,
            key=lambda task: (
                task.preferred_time is None,
                task.preferred_time or time.min,
            ),
        )

    def create_schedule(self, owner: Owner) -> list[Task]:
        """Collect an owner's pet tasks and return them sorted by preferred time.

        Tasks without a preferred time appear after timed tasks.
        """
        return self.sort_by_time(owner.get_all_tasks())


# Preserve imports used by earlier versions of the starter.
task = Task
pet = Pet
owner = Owner
scheduler = Scheduler