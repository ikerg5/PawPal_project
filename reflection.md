# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

1. Set up their profile and pet — The user enters basic info like their name, their pet's name, and how many minutes they have available in a day. This gives the app the context it needs to make a realistic plan.

2. Add care tasks — The user can add things their pet needs that day, like a walk, feeding, or giving medicine. Each task has a name, how long it takes, and how important it is (high, medium, or low priority).

3. Generate a daily schedule — Once the tasks are added, the user clicks a button and the app figures out which tasks fit in the available time, puts the most important ones first, and shows a clear plan for the day.

I ended up with four classes, each doing one job:

- **Owner** — the person using the app. Holds their name and how many minutes they have available, and owns the pets.
- **Pet** — a pet's name, species, and the list of tasks assigned to it.
- **Task** — one care activity: title, duration, priority, whether it's done yet. It doesn't do anything smart on its own, it just holds data.
- **Scheduler** — the "brain." It takes the tasks and figures out the order and what fits in the available time.
- **DailyPlan** — the final result: the list of tasks that made the cut, plus the total time used.

I kept `Scheduler` (the decision-making) separate from `DailyPlan` (the result) so I could change how the scheduling works later without having to change how the plan gets displayed.

**b. Design changes**

I asked my AI assistant to look over `pawpal_system.py` and check for anything missing. It pointed out that `Scheduler` and `DailyPlan` had no way of knowing which pet a plan was actually for — there was no pet name anywhere in those classes, even though the sample output in the README ("Daily plan for Biscuit...") needed that info to make sense.

So I added a pet name (and species) to both classes so the final schedule can actually say whose plan it is. I kept it as just a name/string instead of passing the whole `Pet` object in, since `Scheduler` really only needs the name for display, not the whole object.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler cares about three things: **priority** (high/medium/low), how many **minutes the owner has available**, and each task's **scheduled time** (used for putting things in order and catching conflicts).

Priority and available time matter the most because that's the actual problem a busy pet owner has — not enough time for everything. So if not all tasks fit, the important ones (like feeding) should win a spot over the "nice to have" ones (like brushing). That's why the scheduler sorts by priority first, then cuts things off once it runs out of time, instead of the other way around.

**b. Tradeoffs**

My conflict checker (`detect_conflicts()`) only catches tasks that start at the **exact same time**. It doesn't check if tasks actually overlap. So a 30-minute walk at 08:00 and a 10-minute feeding at 08:15 wouldn't get flagged, even though the walk is technically still happening.

I went with the simple exact-match version because it's easy to write, easy to understand, and fast. The downside is it misses real overlaps that don't start at the same minute. I think that's an okay tradeoff for now since most tasks in this app get typed in by hand and exact-time clashes are the most obvious/common mistake to catch — but a better version would need to actually compare start and end times against each other instead of just grouping by one time string.

I also asked my AI assistant if this method could be written more "Pythonic," and it suggested a version using `collections.defaultdict` and a list comprehension. I decided not to use it — it was a bit shorter, but it crammed everything into one dense expression that's harder to read at a glance. I kept my original loop version since it's easier to follow step by step, which felt more important than saving a couple lines.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI assistant through basically every step of building this: turning my UML sketch into class stubs, writing the actual scheduling logic, hooking the Streamlit UI up to the backend, writing tests, and cleaning up the docs. I kept each phase in a separate conversation like the instructions suggested, and that actually helped — when I was working on tests, the assistant wasn't stuck thinking about UI stuff from earlier.

The thing that helped most was having it actually run the code after every change instead of just writing it and trusting it worked — that caught real bugs, like double-checking the recurring task date math actually added the right number of days. Asking specific questions also worked way better than vague ones. "How should Scheduler get tasks from Owner's pets?" got me a real answer I could evaluate. "Make the scheduler smarter" wouldn't have.

**b. Judgment and verification**

Like I mentioned above, I didn't accept the "more Pythonic" rewrite of `detect_conflicts()` — I checked that both versions gave the same output, then picked the one that was easier to read, not the shorter one.

Being the one steering the project meant I had to make the actual design calls myself — like deciding `Scheduler` should hold onto the `Owner` object instead of just a plain list of tasks, so it always stays up to date if I add more pets later. The AI didn't suggest that on its own; I had to ask for it and decide it made sense. The big lesson for me: AI is really fast at writing code, but I still have to actually run it and check it does what I meant, not just skim the code and assume it's right.

---

## 4. Testing and Verification

**a. What you tested**

My test suite (`tests/test_pawpal.py`, 10 tests total) covers: marking a task done and adding tasks to a pet, sorting tasks by time (including with an empty list), completing a daily task correctly creates tomorrow's task (and a one-time task doesn't create anything), the conflict checker correctly catches a same-time clash and correctly finds nothing when times are different, filtering with no matches, and generating a plan for an owner with no pets yet. I focused on these because they're the parts of the app where a small mistake (like the date math being off by a day) wouldn't be obvious just from reading the code — I needed the tests to actually catch it.

**b. Confidence**

I'd give it about 4 out of 5 stars. The core stuff — sorting, filtering, recurring tasks, and exact-time conflicts — all work and are backed by passing tests. If I had more time I'd want to test: real overlapping time ranges (not just exact matches), what happens if a recurring task keeps getting completed over and over (does the date keep advancing correctly each time?), and the edge case where a task's duration lands exactly on the available time limit.

---

## 5. Reflection

**a. What went well**

I'm happiest with how the `Owner` / `Pet` / `Task` / `Scheduler` split held up as I kept adding features. Going from one pet to multiple pets, and from a simple task list to a scheduler that pulls live data from the owner, only meant extending the existing classes — I never had to tear anything down and start over. The Streamlit UI also connects cleanly to the same methods the CLI demo and tests use, so there's really only one version of the logic, not a UI copy and a "real" copy.

**b. What you would improve**

The main thing I'd fix is the conflict checker only catching exact time matches instead of real overlaps — that's the biggest gap. I'd also want the UI to let you actually filter the task list by pet or by status, instead of always just showing everything sorted by time.

**c. Key takeaway**

The biggest thing I learned is that working with AI works best in small steps — build one thing, run it, check it, then move to the next thing — instead of asking for the whole system at once. That's how I caught the missing pet-name bug early and made a real decision about the conflict-detection tradeoff instead of just accepting whatever came out first. Being the one in charge meant I had to make the actual calls about what each class should be responsible for and which shortcuts were okay for this project — the AI could write the code fast, but it couldn't decide that stuff for me, and it couldn't replace actually running the program to see if it worked.
