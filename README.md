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

## ✨ Features

- **Multi-pet management** — one owner can track any number of pets, each with its own task list
- **Priority-based scheduling** — `Scheduler.generate_plan()` sorts tasks high → medium → low priority and greedily fits as many as possible into the owner's available minutes
- **Sorting by time** — `Scheduler.sort_by_time()` orders tasks chronologically by their `"HH:MM"` scheduled time
- **Filtering** — `Scheduler.filter_by_pet()` and `filter_by_status()` narrow the task list down to one pet or one completion state
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any tasks scheduled at the same time (even across different pets) and surfaces a warning instead of silently double-booking
- **Daily recurrence** — completing a `"daily"` or `"weekly"` task automatically creates the next occurrence, due exactly 1 day or 1 week later, via `Task.next_occurrence()` and `Pet.complete_task()`

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
$ python main.py
Today's Schedule for Jordan
---------------------------
  [ ] [Biscuit] Morning walk (30 min, high priority)
  [ ] [Biscuit] Feeding (10 min, high priority)
  [ ] [Mochi] Litter box cleaning (10 min, medium priority)

Total time used: 50 minutes
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The suite (`tests/test_pawpal.py`) covers:
- **Basic behaviors**: marking a task complete, adding a task increases a pet's task count
- **Sorting**: `sort_by_time()` returns chronological order, and handles an empty task list
- **Recurrence**: completing a `"daily"` task auto-creates the next day's occurrence; completing a `"once"` task creates nothing
- **Conflict detection**: two tasks at the same time are flagged; tasks at different times are not
- **Filtering edge cases**: filtering by a pet/status with no matches returns an empty list rather than erroring
- **Empty state**: generating a plan for an owner with no pets returns an empty, zero-duration plan

Sample test output:

```
$ python -m pytest -v
============================= test session starts ==============================
collected 10 items

tests/test_pawpal.py::test_mark_complete_changes_task_status PASSED      [ 10%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 20%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 30%]
tests/test_pawpal.py::test_sort_by_time_on_empty_list_returns_empty_list PASSED [ 40%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_occurrence PASSED [ 50%]
tests/test_pawpal.py::test_completing_a_one_time_task_creates_no_next_occurrence PASSED [ 60%]
tests/test_pawpal.py::test_detect_conflicts_flags_tasks_at_the_same_time PASSED [ 70%]
tests/test_pawpal.py::test_detect_conflicts_finds_none_when_times_differ PASSED [ 80%]
tests/test_pawpal.py::test_filter_by_pet_with_no_matches_returns_empty_list PASSED [ 90%]
tests/test_pawpal.py::test_generate_plan_for_owner_with_no_pets_returns_empty_plan PASSED [100%]

============================== 10 passed in 0.02s ===============================
```

**Confidence Level:** ⭐⭐⭐⭐☆ (4/5) — core sorting, filtering, recurrence, and exact-time conflict detection are all verified. The main known gap (see `reflection.md` 2b) is that conflict detection only catches exact time matches, not overlapping durations, so that's the main scenario not yet covered by tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority | `Scheduler.sort_by_priority()` | Orders tasks high → medium → low |
| Sort by time | `Scheduler.sort_by_time()` | Orders tasks by their `"HH:MM"` scheduled time; untimed tasks sort last |
| Filtering by pet | `Scheduler.filter_by_pet()` | Returns only the tasks belonging to a given pet |
| Filtering by status | `Scheduler.filter_by_status()` | Returns only tasks matching a completion status |
| Time-budget filtering | `Scheduler.filter_by_time()` | Greedily keeps tasks that fit within the owner's available minutes |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the same scheduled time and returns warning strings (does not crash); only checks exact time matches, not overlapping durations — see `reflection.md` section 2b |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `"daily"`/`"weekly"` task automatically creates its next occurrence, with `due_date` advanced via `timedelta` |

## 📸 Demo Walkthrough

### UI features and available actions

The Streamlit app (`app.py`) lets a user:

- Set their **owner name** and **available minutes** for the day
- **Add pets** (name + species), shown in a running table with each pet's task count
- **Add tasks** to a specific pet, including title, duration, priority, an optional scheduled time, and a frequency (`once`/`daily`/`weekly`)
- View the **current task list sorted chronologically by time**
- See a **warning banner** immediately if two tasks land at the same time, before even generating a schedule
- **Check off tasks as done** — completing a recurring task automatically creates and reports its next occurrence
- Click **"Generate schedule"** to build and display the day's time-boxed plan

### Example workflow

1. Enter the owner's name and available minutes (e.g., "Jordan", 60 minutes).
2. Add two pets: "Biscuit" (dog) and "Mochi" (cat).
3. Add tasks for each pet with different times and priorities — including one deliberate clash, e.g. both pets with a task at 08:00.
4. Notice the conflict warning appear above the task list as soon as the clash exists.
5. Check off a daily task as "Done" and see a confirmation that tomorrow's occurrence was created automatically.
6. Click "Generate schedule" to see the final plan: highest-priority tasks first, cut off once the available minutes run out.

### Key Scheduler behaviors shown

- **Sorting** — tasks display in time order (`Scheduler.sort_by_time()`) and get prioritized high → low when building the plan (`Scheduler.sort_by_priority()`)
- **Conflict warnings** — `Scheduler.detect_conflicts()` catches the same-time clash and surfaces it as a banner
- **Recurrence** — `Pet.complete_task()` auto-spawns tomorrow's/next week's task when a recurring task is checked off

### Sample CLI output (`python main.py`)

```
All tasks sorted by time:
  08:00  [ ] [Biscuit] Morning walk (30 min, high priority)
  08:00  [ ] [Mochi] Feeding (10 min, high priority)
  09:00  [ ] [Mochi] Litter box cleaning (10 min, medium priority)
  12:30  [ ] [Biscuit] Brushing (15 min, low priority)
  17:00  [ ] [Mochi] Playtime (20 min, medium priority)
  18:00  [ ] [Biscuit] Feeding (10 min, high priority)

Biscuit's tasks only (filter_by_pet):
  [ ] [Biscuit] Feeding (10 min, high priority)
  [ ] [Biscuit] Morning walk (30 min, high priority)
  [ ] [Biscuit] Brushing (15 min, low priority)

Incomplete tasks only (filter_by_status):
  [ ] [Biscuit] Feeding (10 min, high priority)
  [ ] [Biscuit] Morning walk (30 min, high priority)
  [ ] [Biscuit] Brushing (15 min, low priority)
  [ ] [Mochi] Playtime (20 min, medium priority)
  [ ] [Mochi] Litter box cleaning (10 min, medium priority)
  [ ] [Mochi] Feeding (10 min, high priority)

Conflict check:
  WARNING: Conflict at 08:00 — Biscuit: Morning walk, Mochi: Feeding

Today's Schedule for Jordan
---------------------------
  [ ] [Biscuit] Feeding (10 min, high priority)
  [ ] [Biscuit] Morning walk (30 min, high priority)
  [ ] [Mochi] Feeding (10 min, high priority)
  [ ] [Mochi] Litter box cleaning (10 min, medium priority)

Total time used: 60 minutes

Completing Biscuit's daily 'Morning walk'...
  Completed: [x] [Biscuit] Morning walk (30 min, high priority) (was due 2026-07-07)
  Next occurrence auto-created: [ ] [Biscuit] Morning walk (30 min, high priority) (due 2026-07-08)
  Biscuit now has 4 tasks
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
