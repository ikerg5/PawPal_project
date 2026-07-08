from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Jordan", available_minutes=60)

    dog = Pet(name="Biscuit", species="Golden Retriever")
    cat = Pet(name="Mochi", species="Cat")

    # Added out of chronological order on purpose, to prove sort_by_time() works.
    dog.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="18:00"))
    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"))
    dog.add_task(Task(title="Brushing", duration_minutes=15, priority="low", time="12:30"))
    cat.add_task(Task(title="Playtime", duration_minutes=20, priority="medium", time="17:00"))
    cat.add_task(Task(title="Litter box cleaning", duration_minutes=10, priority="medium", time="09:00"))
    # Deliberately clashes with Biscuit's 08:00 Morning walk to trigger a conflict warning.
    cat.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time="08:00"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    print("All tasks sorted by time:")
    for task in scheduler.sort_by_time(all_tasks):
        print(f"  {task.time}  {task.display()}")

    print("\nBiscuit's tasks only (filter_by_pet):")
    for task in scheduler.filter_by_pet(all_tasks, "Biscuit"):
        print(f"  {task.display()}")

    print("\nIncomplete tasks only (filter_by_status):")
    for task in scheduler.filter_by_status(all_tasks, is_complete=False):
        print(f"  {task.display()}")

    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts found.")

    print()
    plan = scheduler.generate_plan()
    print(plan.display())

    # Recurring tasks: completing a daily task should auto-create tomorrow's occurrence.
    print("\nCompleting Biscuit's daily 'Morning walk'...")
    morning_walk = next(t for t in dog.tasks if t.title == "Morning walk")
    morning_walk.frequency = "daily"
    next_walk = dog.complete_task(morning_walk)
    print(f"  Completed: {morning_walk.display()} (was due {morning_walk.due_date})")
    print(f"  Next occurrence auto-created: {next_walk.display()} (due {next_walk.due_date})")
    print(f"  Biscuit now has {dog.task_count} tasks")


if __name__ == "__main__":
    main()
