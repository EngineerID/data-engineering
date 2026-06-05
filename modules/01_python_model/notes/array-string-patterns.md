# Reusable Patterns: Arrays & Strings

> **Where this sits in the module.** This is the **algorithmic-reasoning track** of
> Module 01 — the external "Data Structures & Algorithms" strand of the curriculum
> ([`docs/curriculum.md` — Module 2 — DSA](../../../docs/curriculum.md#module-2--data-structures-algorithms--problem-decomposition))
> given a home here. It assumes you can read the Python in
> [`python-foundations.md`](python-foundations.md). It is *parallel* to the
> language-model / OOP track proven in [`../exercises.py`](../exercises.py): one
> builds problem-decomposition instinct, the other builds data-model fluency, and
> both stand on the same foundations rung. See the module
> [`README.md`](../README.md) for the full ladder.

Four transferable techniques extracted from the five examples, plus the
trade-offs that tell you which one to reach for.

Each example, its pattern(s), and time / space cost:

- **Two Sum** — complement hash map · O(n) time, O(n) space.
- **Longest Substring w/o Repeat** — variable sliding window (jump-contract) · O(n) time, O(min(n, alphabet)) space.
- **Container With Most Water** — converging two pointers (greedy bottleneck) · O(n) time, O(1) space.
- **3Sum** — sort + fix-one + converging two pointers + dedup · O(n²) time, O(1) space\*.
- **Char Replacement** — variable sliding window (incremental-contract) · O(n) time, O(alphabet) space.

\* excluding the output list and sort's stack.

**When to reach for each pattern:**

1. **Complement hash map** — when you'd nest two loops to find an element with a fixed relationship to the current one, and you need O(n) and/or original indices.
2. **Variable sliding window** — when you want the longest/shortest/count of a *contiguous* run meeting a constraint.
3. **Converging two pointers** — when the data is sorted/symmetric and one comparison tells you which end to advance.
4. **Sort + fix-one + dedup** — when you need *unique* combinations (pairs, triplets, k-tuples) hitting a target.

---

## 1. Complement hash map (trade space for a second loop)

**Reach for it when** you'd otherwise nest two loops to find an element that
stands in a fixed relationship to the current one (sums to a target, equals a
difference, etc.).

**Key insight.** Scan once. Store each element keyed by whatever you'll later
query. For the current element, derive the partner you *need* and check whether
it's already stored. The map answers "have I seen X?" in O(1), collapsing the
inner loop.

**Invariant that makes it correct.** Check *before* you insert. When you reach
index `i`, the map holds only earlier elements, so an element can never be
paired with itself.

```python
seen = {}
for i, x in enumerate(nums):
    need = target - x
    if need in seen:
        return [seen[need], i]
    seen[x] = i          # record only after the check
```

**Generalizes to:** subarray-sum-equals-k (store prefix sums), "duplicate within
k indices," grouping by a computed key. Note this is also *why* Two Sum doesn't
sort — sorting would destroy the original indices it must return.

---

## 2. Variable-size sliding window

**Reach for it when** you want the longest / shortest / count of a *contiguous*
subarray or substring meeting some constraint.

**Key insight.** Two indices bound a window `start..end`. `end` always advances
(expand). When the window breaks the constraint, advance `start` (contract).
Track the best window as you go. Window length is always `end - start + 1`.

Two contraction styles appear in the examples:

**Incremental contraction** — shrink while invalid, fixing bookkeeping each step.

```python
start = 0
for end in range(len(s)):
    add(s[end])
    while invalid():            # use `if` when one step always restores validity
        remove(s[start])
        start += 1
    best = max(best, end - start + 1)
```

*Char Replacement subtlety:* `max_freq` is never decremented. That's
intentional — the window only ever needs to grow past its best size, so a
slightly stale `max_freq` can't produce a wrong (larger) answer.

**Jump contraction** — leap `start` directly past a known bad position instead
of stepping.

```python
if char in last and last[char] >= start:   # guard: ignore stale indices
    start = last[char] + 1
last[char] = end
```

The `>= start` guard matters: without it, an index from *before* the current
window could drag `start` backward.

---

## 3. Converging two pointers

**Reach for it when** the data is sorted (or symmetric) and a single comparison
lets you decide which end to advance. Each move discards a whole class of
candidates, giving O(n) instead of O(n²).

```python
left, right = 0, len(a) - 1
while left < right:
    evaluate(a[left], a[right])
    if move_left_condition:
        left += 1
    else:
        right -= 1
```

The two decision rules in the examples:

- **Greedy bottleneck (Container With Most Water).** Area is capped by the
  *shorter* line, so moving the taller pointer can only shrink width without
  raising the cap — it's strictly dominated. Always move the shorter side. This
  is the proof that the greedy step is safe.
- **Sorted-sum steering (3Sum inner loop).** Sum too small → move `left` up to
  increase it; too big → move `right` down; equal → record. Sortedness is what
  makes the direction unambiguous.

---

## 4. Sort + fix-one + skip duplicates

**Reach for it when** you need unique combinations (pairs, triplets, k-tuples)
hitting a target.

**Key insight.** Sort first. Sorting buys you two things at once: it enables the
converging two-pointer search above, *and* it places equal values next to each
other so duplicates are skippable with a neighbor comparison. Fix the outer
element in a loop and reduce the rest to a smaller problem (3Sum = fixed `i` +
two-pointer 2Sum).

Deduplication happens at two levels, and you need *both*: the outer skip stops
you from re-anchoring on a value you've already exhausted (which would re-find
every triplet starting with it), while the inner skip stops a single anchor from
recording the same triplet twice when equal values sit side by side.

```python
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i - 1]:   # outer: don't reuse an anchor value
        continue
    left, right = i + 1, len(nums) - 1
    while left < right:
        ...
        else:                               # on a hit, skip equal neighbors
            res.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left]  == nums[left + 1]:  left  += 1
            while left < right and nums[right] == nums[right - 1]: right -= 1
            left += 1; right -= 1
```

**Generalizes to:** 4Sum (add another fixed loop), kSum (recurse down to the
two-pointer base case).

---

## Cross-cutting takeaways

- **Map vs. sort is a real fork.** Use a hash map when you must keep original
  indices and want O(n) (Two Sum). Sort when you need ordering for dedup or
  two-pointer steering and indices don't matter (3Sum). You rarely get both.
- **Every "max" problem here updates `best = max(best, current)` each
  iteration** — the running answer is maintained, never recomputed at the end.
- **"Check before insert"** (pattern 1) and **the stale-index guard**
  (pattern 2, jump style) are the two easiest correctness bugs to introduce;
  both are about not letting an element interact with itself or with state
  outside the current window.
- **Pattern 3 lives inside pattern 4.** Two pointers is a standalone tool *and*
  the inner engine of the sort-based combination search — recognizing that
  nesting is what turns 2Sum into 3Sum into kSum.

---

## The same dedup idea, one altitude up (SQL)

The "sort so equal values sit side by side, then skip neighbours" move in
pattern 4 is the *array* form of an idea you'll meet again in
[Module 02's dedup-keep-latest view](../../02_sql_relational/sql/04_window_patterns.sql)
and its [analytical-SQL patterns note](../../02_sql_relational/notes/sql-patterns.md):
`ROW_NUMBER() OVER (PARTITION BY key ORDER BY …)` then keep `rn = 1`. Different
syntax, identical reasoning — partition the equal things together, keep one
representative per group. Recognising one idea across two stacks is exactly the
transfer this repo is built to train.
