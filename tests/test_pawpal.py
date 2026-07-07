from pawpal_system import Pet, Task


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
