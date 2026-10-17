"""Run a sample multi-pet care schedule."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    pepper = Pet("Pepper", "cat")
    owner.add_pet(mochi)
    owner.add_pet(pepper)

    mochi.add_task(
        Task(
            description="Morning walk",
            frequency="daily",
            duration_minutes=30,
            preferred_time=time(8, 0),
        )
    )
    pepper.add_task(
        Task(
            description="Breakfast",
            frequency="daily",
            duration_minutes=10,
            preferred_time=time(8, 0),
        )
    )
    mochi.add_task(
        Task(
            description="Evening feeding",
            frequency="daily",
            duration_minutes=15,
            preferred_time=time(18, 0),
        )
    )

    print("Today's Schedule")
    print(f"Care plan for {owner.name}")
    scheduler = Scheduler()
    tasks = scheduler.create_schedule(owner)
    for task in tasks:
        scheduled_time = task.preferred_time.strftime("%I:%M %p").lstrip("0")
        pet_name = task.pet.name if task.pet is not None else "Unassigned"
        print(
            f"{scheduled_time} - {task.description} "
            f"({pet_name}, {task.duration_minutes} min, {task.frequency})"
        )

    for warning in scheduler.conflict_warnings(tasks):
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()