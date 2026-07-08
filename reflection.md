# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

1. Set up their profile and pet — The user enters basic info like their name, their pet's name, and how many minutes they have available in a day. This gives the app the context it needs to make a realistic plan.

2. Add care tasks — The user can add things their pet needs that day, like a walk, feeding, or giving medicine. Each task has a name, how long it takes, and how important it is (high, medium, or low priority).

3. Generate a daily schedule — Once the tasks are added, the user clicks a button and the app figures out which tasks fit in the available time, puts the most important ones first, and shows a clear plan for the day.

I included four classes, each with a single, clear responsibility:

- **Owner** — holds the user's identity and their available time budget (`name`, `available_minutes`). It's responsible for owning a `Pet` and exposing `add_pet()`.
- **Pet** — holds the pet's identity (`name`, `species`) and the list of `Task`s that apply to it. Responsible for `add_task()`.
- **Task** — a simple data container (`title`, `duration_minutes`, `priority`, `is_recurring`) with a `display()` method to render one task. It has no behavior beyond describing itself — all decision-making lives in `Scheduler`.
- **Scheduler** — takes a list of tasks and the available minutes and is responsible for turning them into an ordered, time-boxed plan (`sort_by_priority()`, `filter_by_time()`, `generate_plan()`). This keeps scheduling logic out of `Pet`/`Task` so those stay simple data holders.
- **DailyPlan** — the output object: the final ordered list of tasks that fit in the day, plus the total time used, and a `display()` method for showing the result to the user.

Splitting `Scheduler` (decision-making) from `DailyPlan` (result) means the scheduling algorithm can change without touching how a plan is displayed.

**b. Design changes**

After asking my AI assistant to review `pawpal_system.py` for missing relationships or logic bottlenecks, it flagged that `Scheduler` and `DailyPlan` had no way to know which pet the plan was for — there was no `pet_name`/`species` field anywhere in those two classes, even though the README's sample output ("Daily plan for Biscuit (Golden Retriever):") requires that context to render the plan.

I fixed this by adding `pet_name` and `species` fields to both `Scheduler.__init__` and `DailyPlan.__init__`, so the final `display()` output can include which pet the plan belongs to. I chose to pass these as plain strings (rather than passing the whole `Pet` object into `Scheduler`) to keep `Scheduler` decoupled from the `Pet`/`Owner` classes — it only needs the pet's name and species for display, not the full object.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only checks for **exact time matches** (two tasks with the identical `"HH:MM"` string) rather than checking whether task durations actually *overlap*. For example, a 30-minute walk starting at 08:00 and a 10-minute feeding starting at 08:15 would not be flagged, even though the walk is still in progress when the feeding starts.

I chose exact-match checking because it's simple, fast (an O(n) grouping by time string), and easy to reason about, which matters for a first pass at conflict detection. The tradeoff is that it will miss genuine overlaps that don't share a start time. This is reasonable for now because most pet care tasks in this app are short and manually scheduled by the owner, so exact clashes are the most common and most obviously avoidable case — but a more accurate version would need to compare `[start, start + duration]` time ranges pairwise instead of just grouping by a single time string.

I also considered rewriting `detect_conflicts()` with a `collections.defaultdict` and a list comprehension instead of the explicit loop with `setdefault()`. I kept the explicit loop version — it's a few lines longer, but reads top-to-bottom in the order the logic actually executes (group, then filter, then format), which matters more than saving a few lines in a project meant to be read and graded.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
