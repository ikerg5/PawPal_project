import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant. Set up your profile and pets,
add care tasks, then generate a daily schedule that fits your available time.
"""
)

# --- Session "memory" -------------------------------------------------------
# Streamlit reruns this whole script on every interaction, so we keep the
# Owner (and everything hanging off it) in st.session_state instead of
# recreating it — otherwise it would be wiped on every click.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)

owner: Owner = st.session_state.owner

st.divider()

# --- Owner setup -------------------------------------------------------------
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_minutes = st.number_input(
        "Available minutes today", min_value=1, max_value=600, value=owner.available_minutes
    )

st.divider()

# --- Add a pet ---------------------------------------------------------------
st.subheader("Pets")

with st.form("add_pet_form", clear_on_submit=True):
    st.caption("Add a pet")
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        new_pet_name = st.text_input("Pet name", value="")
    with pcol2:
        new_species = st.selectbox("Species", ["dog", "cat", "other"])

    if st.form_submit_button("Add pet"):
        if new_pet_name.strip():
            owner.add_pet(Pet(name=new_pet_name.strip(), species=new_species))
        else:
            st.warning("Enter a pet name before adding.")

if owner.pets:
    st.table(
        [{"name": pet.name, "species": pet.species, "tasks": pet.task_count} for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task ---------------------------------------------------------------
st.subheader("Tasks")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        st.caption("Add a care task for one of your pets")
        pet_names = [pet.name for pet in owner.pets]
        selected_pet_name = st.selectbox("Pet", pet_names)

        tcol1, tcol2, tcol3 = st.columns(3)
        with tcol1:
            task_title = st.text_input("Task title", value="Morning walk")
        with tcol2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with tcol3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        if st.form_submit_button("Add task"):
            selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
            selected_pet.add_task(
                Task(title=task_title, duration_minutes=int(duration), priority=priority)
            )

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": task.pet_name,
                    "title": task.title,
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                }
                for task in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate schedule ---------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()
    st.code(plan.display())
