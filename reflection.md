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

The scheduler considers three constraints: **priority** (high/medium/low), the owner's **available minutes** for the day, and each task's **scheduled time** (`"HH:MM"`, used for chronological ordering and conflict detection).

Priority and available time mattered most because they map directly to the scenario: a busy pet owner has a hard time budget, and if not everything fits, the most important care tasks (feeding, meds) should be guaranteed a slot before "nice to have" ones (brushing) get dropped. That's why `generate_plan()` sorts by priority *before* filtering by time — a low-priority task added first should never bump a high-priority one out of the plan.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only checks for **exact time matches** (two tasks with the identical `"HH:MM"` string) rather than checking whether task durations actually *overlap*. For example, a 30-minute walk starting at 08:00 and a 10-minute feeding starting at 08:15 would not be flagged, even though the walk is still in progress when the feeding starts.

I chose exact-match checking because it's simple, fast (an O(n) grouping by time string), and easy to reason about, which matters for a first pass at conflict detection. The tradeoff is that it will miss genuine overlaps that don't share a start time. This is reasonable for now because most pet care tasks in this app are short and manually scheduled by the owner, so exact clashes are the most common and most obviously avoidable case — but a more accurate version would need to compare `[start, start + duration]` time ranges pairwise instead of just grouping by a single time string.

I also considered rewriting `detect_conflicts()` with a `collections.defaultdict` and a list comprehension instead of the explicit loop with `setdefault()`. I kept the explicit loop version — it's a few lines longer, but reads top-to-bottom in the order the logic actually executes (group, then filter, then format), which matters more than saving a few lines in a project meant to be read and graded.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant across every phase of the build: turning the Mermaid UML into Python class stubs, implementing the scheduling algorithms, wiring the Streamlit UI to the backend, writing the test suite, and drafting documentation. Keeping each phase in its own conversation (as the project instructions suggested) was genuinely useful for staying organized — it meant the assistant's attention in the "testing" phase, for example, wasn't cluttered with earlier back-and-forth about UI layout, and I could reference exactly the right files for the task at hand instead of it re-surfacing stale context.

The most effective feature was having the assistant actually *run* the code after every change (`python main.py`, `pytest`) rather than just writing it and moving on — this caught things a code review alone wouldn't, like confirming the recurring-task date math actually advanced by the right number of days. The most helpful prompts were the ones that referenced concrete files and asked a specific architectural question — e.g. "how should Scheduler retrieve tasks from Owner's pets?" — rather than vague asks like "make the scheduler smarter." Specific questions got specific, evaluable answers.

**b. Judgment and verification**

When asked to evaluate `detect_conflicts()` for readability, the assistant offered a more "Pythonic" rewrite using `collections.defaultdict` and a list comprehension. I rejected it and kept the original explicit loop — the comprehension version was a few lines shorter but crammed the grouping, filtering, and string formatting into one nested expression, which is harder to scan for a grader or a future reader than the loop's plain top-to-bottom order. I verified both versions actually produced identical warning output before deciding, so the choice was about readability, not correctness.

**Being the "lead architect":** the assistant is fast at producing plausible, working code, but it doesn't know *why* a design choice matters to this specific app unless I supply that context — e.g., deciding `Scheduler` should hold an `Owner` reference (not a raw task list) so it stays in sync with pets added after construction was a judgment call I had to make and direct, not something the assistant volunteered unprompted. The main lesson: AI accelerates the "write it" step, but verifying it actually does what's intended — by running it, not just reading the diff — stays a human responsibility.

---

## 4. Testing and Verification

**a. What you tested**

The test suite (`tests/test_pawpal.py`, 10 tests) covers: marking a task complete and adding a task to a pet (basic behaviors), `sort_by_time()` chronological ordering including an empty list, `Pet.complete_task()` correctly spawning the next occurrence for a `"daily"` task and creating nothing for a `"once"` task, `detect_conflicts()` correctly flagging a same-time clash and correctly finding none when times differ, filtering by pet/status with no matches, and generating a plan for an owner with zero pets. These mattered because they're exactly the algorithmic behaviors added in Phase 4 that have no visible feedback loop other than trusting the code — a subtly wrong `timedelta` or an off-by-one in the conflict grouping would be easy to miss just by reading the code.

**b. Confidence**

⭐⭐⭐⭐☆ (4/5). Core sorting, filtering, recurrence, and exact-time conflict detection are all verified by passing tests and by manually running `main.py`/the Streamlit app. If I had more time, I'd test: overlapping-but-not-identical time ranges (the known gap from section 2b), what happens when a recurring task keeps completing multiple times in a row (does the chain of `due_date`s stay correct?), and the exact boundary case where a task's duration brings `time_used` to precisely equal `available_minutes`.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the `Owner → Pet → Task` / `Scheduler` split holding up as the design grew — going from a single pet to multiple pets, and from a static task list to a `Scheduler` that pulls live data through `Owner.get_all_tasks()`, only required extending existing classes rather than rearchitecting them. The Streamlit UI integration also went smoothly end-to-end: forms feed directly into the same `Pet.add_task()`/`Pet.complete_task()` methods the CLI demo and tests use, so there's one source of truth for the logic.

**b. What you would improve**

The biggest gap is that `detect_conflicts()` only catches exact time matches, not overlapping durations (documented in section 2b) — a real version of this app would need interval-overlap checking. I'd also want the UI to let an owner sort/filter the task list interactively (by pet, by status) instead of only ever seeing the full list sorted by time.

**c. Key takeaway**

The most important thing I learned is that AI collaboration works best as a tight loop of small, verifiable steps rather than one big "build the whole thing" request — asking for one class, running it, then asking for the next algorithm and running that, caught issues (like the missing `pet_name` context in Phase 1, or the conflict-detection tradeoff in Phase 4) while they were still small and easy to reason about. Being the "lead architect" meant making the calls the assistant couldn't make for me — what the classes should be responsible for, which tradeoffs were acceptable for this scenario — while relying on the assistant to execute those calls quickly and to actually run the result so I could verify it, not just read it.
