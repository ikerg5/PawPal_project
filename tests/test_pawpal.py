from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_task_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Golden Retriever")
    assert pet.task_count == 0

    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    assert pet.task_count == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_minutes=120)
    scheduler = Scheduler(owner)

    tasks = [
        Task(title="Feeding", duration_minutes=10, priority="high", time="18:00"),
        Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"),
        Task(title="Brushing", duration_minutes=15, priority="low", time="12:30"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [t.title for t in sorted_tasks] == ["Morning walk", "Brushing", "Feeding"]


def test_sort_by_time_on_empty_list_returns_empty_list():
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time([]) == []


def test_completing_daily_task_creates_next_day_occurrence():
    pet = Pet(name="Biscuit", species="Golden Retriever")
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        due_date=date(2026, 1, 1),
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.is_complete is False
    assert next_task.due_date == date(2026, 1, 1) + timedelta(days=1)
    assert pet.task_count == 2


def test_completing_a_one_time_task_creates_no_next_occurrence():
    pet = Pet(name="Biscuit", species="Golden Retriever")
    task = Task(title="Vet visit", duration_minutes=45, priority="high", frequency="once")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is None
    assert pet.task_count == 1


def test_detect_conflicts_flags_tasks_at_the_same_time():
    owner = Owner(name="Jordan", available_minutes=120)
    scheduler = Scheduler(owner)

    dog = Pet(name="Biscuit", species="Golden Retriever")
    cat = Pet(name="Mochi", species="Cat")
    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"))
    cat.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="08:00"))

    conflicts = scheduler.detect_conflicts(dog.tasks + cat.tasks)

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_finds_none_when_times_differ():
    owner = Owner(name="Jordan", available_minutes=120)
    scheduler = Scheduler(owner)

    tasks = [
        Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"),
        Task(title="Feeding", duration_minutes=10, priority="high", time="09:00"),
    ]

    assert scheduler.detect_conflicts(tasks) == []


def test_filter_by_pet_with_no_matches_returns_empty_list():
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner)

    tasks = [Task(title="Feeding", duration_minutes=10, priority="high", pet_name="Biscuit")]

    assert scheduler.filter_by_pet(tasks, "Mochi") == []


def test_generate_plan_for_owner_with_no_pets_returns_empty_plan():
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan.scheduled_tasks == []
    assert plan.total_time_used == 0
