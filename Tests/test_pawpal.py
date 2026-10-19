from datetime import datetime, time, timezone

from pawpal_system import Pet, Scheduler, Task


def test_mark_complete_records_task_completion() -> None:
    task = Task("Morning walk", "daily", 30)
    occurrence = datetime(2026, 10, 12, 8, 0)

    next_task = task.mark_complete(occurrence)

    assert occurrence in task.completed_occurrences
    assert next_task is not None
    assert next_task.due_at == datetime(2026, 10, 13, 8, 0)


def test_daily_task_due_date_advances_across_year_boundary() -> None:
    task = Task("Morning walk", "daily", 30)

    next_task = task.mark_complete(datetime(2026, 12, 31, 8, 0))

    assert next_task is not None
    assert next_task.due_at == datetime(2027, 1, 1, 8, 0)


def test_daily_task_due_date_advances_across_leap_day() -> None:
    task = Task("Morning walk", "daily", 30)

    next_task = task.mark_complete(datetime(2028, 2, 28, 8, 0))

    assert next_task is not None
    assert next_task.due_at == datetime(2028, 2, 29, 8, 0)


def test_mark_complete_preserves_timezone_on_next_due_date() -> None:
    task = Task("Morning walk", "daily", 30)
    occurrence = datetime(2026, 10, 16, 8, 0, tzinfo=timezone.utc)

    next_task = task.mark_complete(occurrence)

    assert next_task is not None
    assert next_task.due_at == datetime(2026, 10, 17, 8, 0, tzinfo=timezone.utc)


def test_mark_complete_adds_next_recurring_task_to_same_pet() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Weekly bath", "weekly", 45, preferred_time=time(10, 0))
    pet.add_task(task)

    next_task = task.mark_complete(datetime(2026, 10, 16, 11, 0))

    assert next_task is not None
    assert next_task.due_at == datetime(2026, 10, 23, 10, 0)
    assert pet.tasks[-1] is next_task
    assert next_task.pet is pet


def test_mark_complete_does_not_duplicate_recurring_task_for_same_occurrence() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Daily walk", "daily", 30)
    pet.add_task(task)
    occurrence = datetime(2026, 10, 16, 8, 0)

    first_next_task = task.mark_complete(occurrence)
    second_next_task = task.mark_complete(occurrence)

    assert first_next_task is not None
    assert second_next_task is None
    assert len(pet.tasks) == 2


def test_mark_complete_does_not_create_next_task_for_nonrecurring_task() -> None:
    task = Task("Nail trim", "monthly", 20)

    next_task = task.mark_complete(datetime(2026, 10, 16, 8, 0))

    assert next_task is None


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "daily", 30)

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_sort_by_time_orders_tasks_chronologically_and_puts_untimed_last() -> None:
    late_task = Task("Evening feeding", "daily", 15, preferred_time=time(18, 0))
    untimed_task = Task("Grooming", "weekly", 30)
    early_task = Task("Breakfast", "daily", 10, preferred_time=time(7, 30))

    result = Scheduler().sort_by_time([late_task, untimed_task, early_task])

    assert result == [early_task, late_task, untimed_task]


def test_sort_by_time_is_stable_and_does_not_modify_input() -> None:
    first_at_midnight = Task("Breakfast", "daily", 10, preferred_time=time(0, 0))
    second_at_midnight = Task("Medication", "daily", 5, preferred_time=time(0, 0))
    last_timed_task = Task("Evening walk", "daily", 30, preferred_time=time(23, 59))
    untimed_task = Task("Grooming", "weekly", 30)
    tasks = [second_at_midnight, untimed_task, last_timed_task, first_at_midnight]

    result = Scheduler().sort_by_time(tasks)

    assert result == [
        second_at_midnight,
        first_at_midnight,
        last_timed_task,
        untimed_task,
    ]
    assert tasks == [second_at_midnight, untimed_task, last_timed_task, first_at_midnight]


def test_detect_time_conflicts_for_tasks_assigned_to_the_same_pet() -> None:
    pet = Pet("Mochi", "dog")
    walk = Task("Walk", "daily", 30, preferred_time=time(8, 0))
    medication = Task("Medication", "daily", 5, preferred_time=time(8, 0))
    pet.add_task(walk)
    pet.add_task(medication)

    assert Scheduler().detect_time_conflicts(pet.tasks) == [(walk, medication)]


def test_detect_time_conflicts_returns_every_pair_for_duplicate_times() -> None:
    walk = Task("Walk", "daily", 30, preferred_time=time(8, 0))
    medication = Task("Medication", "daily", 5, preferred_time=time(8, 0))
    feeding = Task("Feeding", "daily", 10, preferred_time=time(8, 0))

    conflicts = Scheduler().detect_time_conflicts([walk, medication, feeding])

    assert conflicts == [
        (walk, medication),
        (walk, feeding),
        (medication, feeding),
    ]


def test_detect_time_conflicts_across_different_pets() -> None:
    first_pet = Pet("Mochi", "dog")
    second_pet = Pet("Pepper", "cat")
    walk = Task("Walk", "daily", 30, preferred_time=time(8, 0))
    feeding = Task("Feeding", "daily", 10, preferred_time=time(8, 0))
    first_pet.add_task(walk)
    second_pet.add_task(feeding)

    assert Scheduler().detect_time_conflicts([walk, feeding]) == [(walk, feeding)]


def test_detect_time_conflicts_ignores_untimed_and_distinct_tasks() -> None:
    timed_task = Task("Walk", "daily", 30, preferred_time=time(8, 0))
    other_timed_task = Task("Feeding", "daily", 10, preferred_time=time(9, 0))
    untimed_task = Task("Grooming", "weekly", 30)

    assert Scheduler().detect_time_conflicts(
        [timed_task, other_timed_task, untimed_task]
    ) == []


def test_conflict_warnings_returns_message_for_matching_times() -> None:
    first_task = Task("Walk", "daily", 30, preferred_time=time(8, 0))
    second_task = Task("Medication", "daily", 5, preferred_time=time(8, 0))

    warnings = Scheduler().conflict_warnings([first_task, second_task])

    assert warnings == [
        "Scheduling conflict at 08:00: 'Walk' and 'Medication' are set for the same time."
    ]


def test_conflict_warnings_returns_empty_list_when_no_conflicts() -> None:
    tasks = [
        Task("Walk", "daily", 30, preferred_time=time(8, 0)),
        Task("Feeding", "daily", 10, preferred_time=time(9, 0)),
        Task("Grooming", "weekly", 20),
    ]

    assert Scheduler().conflict_warnings(tasks) == []


def test_filter_tasks_by_completion_status() -> None:
    completed_task = Task("Medication", "daily", 5)
    incomplete_task = Task("Walk", "daily", 30)
    completed_task.mark_complete(datetime(2026, 10, 16, 8, 0))

    result = Scheduler().filter_tasks(
        [completed_task, incomplete_task],
        completed=False,
    )

    assert result == [incomplete_task]


def test_filter_tasks_by_pet_name_case_insensitively() -> None:
    mochi = Pet("Mochi", "dog")
    pepper = Pet("Pepper", "cat")
    mochi_task = Task("Walk", "daily", 30)
    pepper_task = Task("Feeding", "daily", 10)
    mochi.add_task(mochi_task)
    pepper.add_task(pepper_task)

    result = Scheduler().filter_tasks(
        [mochi_task, pepper_task],
        pet_name="mochi",
    )

    assert result == [mochi_task]