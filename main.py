from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Jordan", available_minutes=60)

    dog = Pet(name="Biscuit", species="Golden Retriever")
    cat = Pet(name="Mochi", species="Cat")

    dog.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
    dog.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    dog.add_task(Task(title="Brushing", duration_minutes=15, priority="low"))
    cat.add_task(Task(title="Litter box cleaning", duration_minutes=10, priority="medium"))
    cat.add_task(Task(title="Playtime", duration_minutes=20, priority="medium"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    print(plan.display())


if __name__ == "__main__":
    main()
