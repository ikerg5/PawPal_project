from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single pet care activity with a duration, priority, and completion status."""

    title: str
    duration_minutes: int
    priority: str          # "high", "medium", or "low"
    is_recurring: bool = False
    is_complete: bool = False
    pet_name: str = ""     # filled in automatically by Pet.add_task()

    def mark_complete(self) -> None:
        """Flip this task's status to complete."""
        self.is_complete = True

    def display(self) -> str:
        """Return a one-line human-readable summary of this task."""
        status = "x" if self.is_complete else " "
        owner_tag = f"[{self.pet_name}] " if self.pet_name else ""
        return f"[{status}] {owner_tag}{self.title} ({self.duration_minutes} min, {self.priority} priority)"


@dataclass
class Pet:
    """A pet and the list of care tasks assigned to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Tag a task with this pet's name and add it to the pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    @property
    def task_count(self) -> int:
        """Return how many tasks are currently assigned to this pet."""
        return len(self.tasks)


@dataclass
class Owner:
    """A pet owner who manages one or more pets and their combined tasks."""

    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Flatten and return every task across all of this owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Organizes an owner's tasks across all their pets into a single daily plan."""

    _PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner):
        """Store the owner whose pets' tasks this scheduler will manage."""
        self.owner = owner

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return the given tasks ordered from highest to lowest priority."""
        return sorted(tasks, key=lambda t: self._PRIORITY_ORDER.get(t.priority, len(self._PRIORITY_ORDER)))

    def filter_by_time(self, sorted_tasks: List[Task]) -> List[Task]:
        """Return the leading tasks that fit within the owner's available minutes."""
        fitted: List[Task] = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                fitted.append(task)
                time_used += task.duration_minutes
        return fitted

    def generate_plan(self) -> "DailyPlan":
        """Pull all tasks from the owner's pets and build a time-boxed DailyPlan."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = self.sort_by_priority(all_tasks)
        fitted_tasks = self.filter_by_time(sorted_tasks)

        plan = DailyPlan(owner_name=self.owner.name)
        for task in fitted_tasks:
            plan.add_task(task)
        return plan


class DailyPlan:
    """The finished, ordered schedule of tasks that fit in a day."""

    def __init__(self, owner_name: str = ""):
        """Start an empty plan for the given owner."""
        self.owner_name = owner_name
        self.scheduled_tasks: List[Task] = []
        self.total_time_used: int = 0

    def add_task(self, task: Task) -> None:
        """Append a task to the plan and add its duration to the running total."""
        self.scheduled_tasks.append(task)
        self.total_time_used += task.duration_minutes

    def display(self) -> str:
        """Return a formatted, terminal-friendly rendering of the day's schedule."""
        header = f"Today's Schedule for {self.owner_name}" if self.owner_name else "Today's Schedule"
        lines = [header, "-" * len(header)]

        if not self.scheduled_tasks:
            lines.append("No tasks scheduled.")
        else:
            for task in self.scheduled_tasks:
                lines.append(f"  {task.display()}")

        lines.append(f"\nTotal time used: {self.total_time_used} minutes")
        return "\n".join(lines)
