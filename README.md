# Algorithms & Unit Test Harness (Tammy Davies, MSc Portfolio · Cardiff University · 2025)

A compact, production-clean showcase of five algorithmic exercises plus a cross-platform, multiprocessing test harness. It demonstrates graph theory, search, recursion/backtracking, lexicographic optimisation, and practical testability.

## Contents

- `exercise1(...)` — **Spacemon Competition**  
  Turn-based duel simulator with elemental multipliers. Preserves winner’s remaining energy; Team 1 moves first.
- `exercise2(...)` — **Five-Letter Unscramble**  
  Counts dictionary words formable from a multiset of letters.
- `exercise3(...)` — **Wordle Set**  
  Applies green/yellow/grey constraints against a word list.
- `exercise4(...)` — **2D Most Rewarding Shortest Path**  
  Finds the shortest `A → B` path; breaks ties by maximising rewards collected.
- `exercise5(...)` — **Social Network Analysis**  
  Enumerates **maximal cliques** via a Bron–Kerbosch-style routine and reports per-node clique membership counts.

**Test Harness** — `testingFramework.py`  
Runs the full suite with per-test timeouts (multiprocessing; ~3s/test by default).

---

## Files & structure

```
.
├─ README.md
├─ template.py            # implementations for exercise1..exercise5
├─ testingFramework.py    # official test harness & cases
└─ wordle.txt             # dictionary required by exercises 2 & 3 (one word per line)
```

> If you prefer splitting implementations, keep `template.py` as the public entry point and import internally.

---

## How to evaluate (tests)

**Prereqs**
- Python **3.9+**
- `wordle.txt` present in the repo root (lowercase, one word per line; five letters recommended)

**Run**
```bash
python3 testingFramework.py template.py
```

If `python3` isn’t available on your system:
```bash
python testingFramework.py template.py
```

You’ll see per-test logs and per-function scores. Example:
```
#### FUNCTION exercise1:

Test: 1
exercise1([...]): PASSED
...
#### FUNCTION exercise1 SCORE: 2 / 2
```

**Notes**
- The harness imports the module passed on the command line (no `.py` extension internally).
- Each test runs in a separate process with a small time budget to guard against runaway execution.

---

## Word list (for exercises 2 & 3)

- File name: **`wordle.txt`**
- Format: one word per line (lowercase ASCII).  
- Changing this list may change the expected counts in certain tests.

Tiny example:
```
cacao
ratio
coast
actor
chaos
```

---

## Design notes

### `exercise1` — Spacemon Competition
- Deterministic turn order; uses a fixed multiplier table.
- Winner’s **remaining energy** is persisted into subsequent duels.
- Complexity proportional to number of attack rounds; bounded by initial energy/power ratios.

### `exercise2` — Five-Letter Unscramble
- Direct multiset containment check using string counts for clarity.
- For larger dictionaries, a `collections.Counter` approach offers better asymptotics.

### `exercise3` — Wordle Set
- 0-indexed positions for green/yellow constraints.
- Ensures presence for yellows while excluding specific positions; hard-excludes greys.

### `exercise4` — 2D Most Rewarding Shortest Path
- Explores 4-connected grid; returns `(min_steps, reward_count)`.
- Implemented via DFS + backtracking, comparing `(steps, -rewards)` lexicographically.
- For large grids, a BFS that prioritises **shortest** paths first, then maximises rewards, is preferable.

### `exercise5` — Social Network Cliques
- Input as an adjacency **matrix** (undirected, simple graph).
- Simplified Bron–Kerbosch sets: `curr_clique`, `to_add`, `to_skip`.
- Reports how many maximal cliques each node belongs to.
- Reference: Bron, C., & Kerbosch, J. (1973). *Algorithm 457: Finding all cliques of an undirected graph.* **CACM, 16(9)**, 575–577.

---

## What to review (fast)

- **`template.py`**: function interfaces, clarity of control flow, and guardrails.
- **`testingFramework.py`**: multiprocessing isolation, timeouts, and deterministic output.
- **Edge-case handling**: out-of-bounds checks, tie-break rules, and dictionary dependency.
- **Comments**: concise, intent-level documentation rather than line-by-line narration.


