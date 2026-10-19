# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# Today's Schedule
# Care plan for Jordan
# 7:30 AM - Breakfast (Pepper, 10 min, daily)
# 8:00 AM - Morning walk (Mochi, 30 min, daily)
# 6:00 PM - Evening feeding (Mochi, 15 min, daily)
```
## Implimentation Summary
The classes descriptions are as follows 
	Task: stores different metrics by which a task is informed or measured
	Pet: owns a list of tasks and ensures a task can only belong to one pet at a time.
	Owner: groups pets together under an owner. It also produces the sum total of tasks for all pets under an owner
	Scheduler: takes an Owner, collects all tasks, and sorts them by preferred time
	
Each class depends on the others . Owner contains Pets, each Pet contains Tasks, and the Scheduler reads the owner’s full task list to produce a care plan.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
=========================== test session starts ============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\vyoji\OneDrive\Documents\ai110_Class_Assignments\ai110-module2show-pawpal-starter
collected 18 items                                                          

Tests\test_pawpal.py ..................                               [100%]

============================ 18 passed in 0.09s ============================
```
Confidence level - 5


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

	Task: stores different metrics by which a task is informed or measured
	Pet: owns a list of tasks and ensures a task can only belong to one pet at a time.
	Owner: groups pets together under an owner. It also produces the sum total of tasks for all pets under an owner
	Scheduler: takes an Owner, collects all tasks, and sorts them by preferred time
	
	Each class depends on the others . Owner contains Pets, each Pet contains Tasks, and the Scheduler reads the owner’s full task list to produce a care plan.
	
	Sorting behavior — Scheduler.sort_by_time() and Scheduler.create_schedule()
	sort_by_time() returns tasks in ascending preferred_time order. Tasks without a preferred time appear last, and tasks with matching times keep their original order. create_schedule() collects tasks from all of an owner’s pets and sorts them using this method.
	
	Filtering behavior — Scheduler.filter_tasks()
	Tasks can be filtered by completion status, pet name, or both. A task counts as completed if it has at least one recorded completion in completed_occurrences. Pet-name matching is case-insensitive, and a task must match both criteria when both are supplied.
	
	Conflict detection — Scheduler.detect_time_conflicts() and Scheduler.conflict_warnings()
	detect_time_conflicts() returns pairs of distinct tasks with the same non-None preferred time, whether they belong to the same pet or different pets. It checks for matching start times only; it does not compare durations to detect overlapping intervals. conflict_warnings() turns those pairs into readable warning messages.
	
	Recurring tasks — Task.mark_complete()
	When a completion is recorded, mark_complete() creates the next task for daily and weekly frequencies, due one or seven days after the supplied completion timestamp. It preserves the preferred time, or uses the completion time if no preferred time is set. If the task belongs to a pet, the new task is attached to that pet.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- The app prompts users to enter pet, owner, and task information -->
2. <!-- Once a pets name has been submitted, the app remebers the pet and will show all the names of added pets when a user goes to give the task details -->
3. <!-- Users tasks are recorded -->
4. <!-- When a user chooses to generate their plan, the app will show a plan involving all of the pets -->
5. <!-- The app will note any time conflicts in the schedule.-->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
