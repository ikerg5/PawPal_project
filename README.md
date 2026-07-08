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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
