from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "high", "medium", or "low"
    is_recurring: bool = False

    def display(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pet: "Pet" = None

    def add_pet(self, pet: "Pet") -> None:
        pass


class Scheduler:
    def __init__(self, tasks: List[Task], available_minutes: int):
        self.tasks = tasks
        self.available_minutes = available_minutes

    def sort_by_priority(self) -> List[Task]:
        pass

    def filter_by_time(self, sorted_tasks: List[Task]) -> List[Task]:
        pass

    def generate_plan(self) -> "DailyPlan":
        pass


class DailyPlan:
    def __init__(self):
        self.scheduled_tasks: List[Task] = []
        self.total_time_used: int = 0

    def add_task(self, task: Task) -> None:
        pass

    def display(self) -> str:
        pass
