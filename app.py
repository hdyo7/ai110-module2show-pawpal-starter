from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def task_table_rows(tasks: list[Task]) -> list[dict[str, str | int]]:
    return [
        {
            "Time": (
                task.preferred_time.strftime("%I:%M %p").lstrip("0")
                if task.preferred_time is not None
                else "Unscheduled"
            ),
            "Task": task.description,
            "Pet": task.pet.name if task.pet is not None else "Unassigned",
            "Duration (min)": task.duration_minutes,
            "Frequency": task.frequency,
        }
        for task in tasks
    ]


st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Create the Owner once so it survives Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name}")

st.markdown("### Tasks")
st.caption("Add care tasks and preferred times to build a schedule.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    preferred_time = st.time_input("Preferred time", value=time(8, 0))
with col4:
    frequency = st.selectbox("Frequency", ["daily", "weekly"])

if owner.pets:
    pet_choice = st.selectbox("Assign to pet", [p.name for p in owner.pets])

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == pet_choice)
        pet.add_task(
            Task(
                description=task_title,
                frequency=frequency,
                duration_minutes=duration,
                preferred_time=preferred_time,
            )
        )
        st.success("Task added")
else:
    st.info("Add a pet first, then you can add tasks.")

scheduler = Scheduler()
tasks = scheduler.create_schedule(owner)
if tasks:
    st.markdown("#### Task overview")
    filter_options = ["All pets", *dict.fromkeys(pet.name for pet in owner.pets)]
    selected_pet = st.selectbox("Filter tasks by pet", filter_options)
    filtered_tasks = scheduler.filter_tasks(
        tasks,
        pet_name=None if selected_pet == "All pets" else selected_pet,
    )
    filtered_tasks = scheduler.sort_by_time(filtered_tasks)
    st.success(f"Showing {len(filtered_tasks)} of {len(tasks)} tasks.")
    if filtered_tasks:
        st.table(task_table_rows(filtered_tasks))
    else:
        st.info("No tasks match this pet filter.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("The scheduler orders tasks by preferred time and flags matching times.")

if st.button("Generate schedule"):
    schedule = scheduler.create_schedule(owner)
    if schedule:
        st.markdown(f"### Care plan for {owner.name}")
        st.table(task_table_rows(schedule))
        warnings = scheduler.conflict_warnings(schedule)
        if warnings:
            for warning in warnings:
                st.warning(warning)
        else:
            st.success("Schedule generated with no matching-time conflicts.")
    else:
        st.info("Add at least one task to generate a schedule.")
