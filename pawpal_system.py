"""Dataclass-based skeleton for the PawPal pet care system."""

from dataclasses import dataclass, field


@dataclass
class Task:
    category: str
    time: str
    completed: bool = False


@dataclass
class Pet:
    name: str
    weight: float
    age: int
    food: str
    medication: list[Task] = field(default_factory=list)
    walks: list[Task] = field(default_factory=list)
    meals: list[Task] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)

    def medication_taken(self) -> int:
        pass

    def walks_taken(self) -> int:
        pass

    def add_allergy(self, allergy: str) -> None:
        pass

    def meal_time(self, time: str) -> None:
        pass

    def meal_type(self, category: str) -> None:
        pass

    def weight_change(self, new_weight: float) -> float:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def care_plan(self, owner: Owner) -> list[Task]:
        pass