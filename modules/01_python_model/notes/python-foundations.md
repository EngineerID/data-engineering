# Python Foundations
### Everything used in the pattern examples — nothing more

> **Where this sits in the module.** This is the **bottom rung** of Module 01 —
> written for someone who has never programmed. Read it first; then
> [`array-string-patterns.md`](array-string-patterns.md) (the algorithmic-reasoning
> track) reads smoothly, and the data-model exercises in
> [`../exercises.py`](../exercises.py) (the OOP / dunder ceiling) make sense on top
> of it. It is scoped deliberately: every section is here because it appears in the
> pattern code, not because Python is broadly large. See the module
> [`README.md`](../README.md) for the full ladder.

This document covers only the Python concepts and idioms needed to comfortably
read the pattern examples that follow. It is not a general Python tutorial —
sections were chosen because each one appears in the code, not because it's
broadly useful. Read it once, then the pattern document will read smoothly.

Each section explains the concept, shows it in isolation, then shows exactly
where it appears in the code.

---

## 1. Variables and assignment

A variable is just a name that holds a value. You create one by writing
`name = value`. The value can be a number, text, a list — anything.

```python
score = 0
name = "Alice"
```

You can change the value of a variable at any time, and you can update it
relative to itself:

```python
score = 0
score = score + 1   # score is now 1
# shorthand:
score += 1          # score is now 2
```

**Where you'll see this:** Every example uses running variables like
`max_length = 0`, `start = 0`, `max_water = 0` that get updated in a loop.

---

## 2. Lists

A list is an ordered collection of items, written with square brackets.
Items can be numbers, strings, other lists — anything.

```python
nums = [2, 7, 11, 15]
```

**Indexing** — access a single item by its position (positions start at 0):

```python
nums[0]   # 2  (first item)
nums[1]   # 7  (second item)
nums[-1]  # 15 (last item — negative counts from the end)
```

**Length** — `len(x)` gives the number of items:

```python
len(nums)   # 4
```

**Appending** — add an item to the end:

```python
result = []
result.append([1, 2, 3])   # result is now [[1, 2, 3]]
```

**Where you'll see this:** `nums` is the input list in most examples.
`res.append(...)` is how 3Sum collects its answer triplets.

---

## 3. Dictionaries (the key data structure in these patterns)

Dictionaries do the heavy lifting in three of the five patterns, for two
reasons: looking up a key is *fast* (effectively instant, no matter how much
you've stored), and a dictionary is *mutable* (you can keep updating it as you
move through a loop). Together that lets you remember what you've already seen
and check against it cheaply — which is exactly what turns a slow nested-loop
solution into a fast single-pass one.

A dictionary stores *key → value* pairs. Think of it like a real dictionary:
you look up a word (the key) and get its definition (the value).

```python
seen = {}              # empty dictionary
seen["a"] = 3          # store: key "a" maps to value 3
seen["b"] = 7

seen["a"]              # 3  (look up key "a")
"a" in seen            # True  (check whether key "a" exists)
"z" in seen            # False
```

You can use numbers or strings as keys.

**`.get(key, default)`** — look up a key, but return a default value if the
key doesn't exist (instead of crashing):

```python
count = {}
count.get("x", 0)      # 0  (key not found, return default)
count["x"] = 5
count.get("x", 0)      # 5  (key found, return actual value)
```

**Where you'll see this:** `seen = {}` in Two Sum stores each number you've
visited. `char_map = {}` in Longest Substring stores the last position of each
character. `count = {}` in Char Replacement stores how often each character
appears in the current window.

> **Ladder note.** The *speed* of dictionary lookup (`x in seen` is O(1)) is the
> whole reason the [hash-map pattern](array-string-patterns.md#1-complement-hash-map-trade-space-for-a-second-loop)
> works, and *why* a number can be a key is the hashability idea proven one rung up
> in `Vector2.__hash__` ([`../exercises.py`](../exercises.py)). Same concept, two
> altitudes.

---

## 4. `if` statements and comparisons

An `if` block runs only when its condition is true.

```python
x = 5

if x > 3:
    print("big")        # this runs

if x > 10:
    print("huge")       # this does not run
```

`elif` and `else` handle other cases:

```python
total = 0

if total < 0:
    print("negative")
elif total > 0:
    print("positive")
else:
    print("zero")       # this runs
```

**Comparison operators:** `==` (equal), `!=` (not equal), `<`, `>`, `<=`, `>=`.

**Combining conditions:** `and` (both must be true), `or` (either can be true).

```python
if i > 0 and nums[i] == nums[i - 1]:
    # both conditions are true
```

**Where you'll see this:** Every example uses `if/elif/else` to decide whether
to update pointers, skip duplicates, or record a result.

---

## 5. `for` loops

A `for` loop repeats a block of code for each item in a sequence.

```python
nums = [10, 20, 30]

for num in nums:
    print(num)
# prints: 10, then 20, then 30
```

**`range(n)`** — produces the integers 0, 1, 2, … n-1. Use it when you need
to loop by index rather than by value:

```python
for i in range(4):
    print(i)
# prints: 0, 1, 2, 3

for i in range(len(nums) - 2):
    # loops from 0 up to but not including len(nums) - 2
```

**`enumerate(sequence)`** — gives you both the index *and* the value on each
iteration:

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)
# 0 a
# 1 b
# 2 c
```

**Where you'll see this:** Two Sum uses `for index, num in enumerate(nums)` to
access each number and know its position at the same time. Char Replacement
uses `for end in range(len(s))` to advance the right edge of the window.

---

## 6. `while` loops

A `while` loop keeps running as long as its condition is true. You control when
it stops by changing a variable inside the loop.

```python
left = 0
right = 4

while left < right:
    print(left, right)
    left += 1
    right -= 1
# 0 4
# 1 3
# 2 2  ← now left < right is false, loop stops
```

Be careful: if the condition never becomes false, the loop runs forever.

**Where you'll see this:** Container With Most Water and 3Sum use
`while left < right` to move two pointers toward each other until they meet.

---

## 7. `continue` and early `return`

**`continue`** — skip the rest of the current loop iteration and jump to the
next one:

```python
for i in range(5):
    if i == 2:
        continue        # skip 2
    print(i)
# prints: 0, 1, 3, 4
```

**`return`** — immediately exit a function and send a value back to the caller.
Once `return` is hit, nothing else in the function runs:

```python
def find_it(nums):
    for num in nums:
        if num == 7:
            return "found it"
    return "not found"
```

**Where you'll see this:** Two Sum uses `return [seen[complement], index]` the
moment it finds its answer. 3Sum uses `continue` to skip anchor values that
have already been used.

---

## 8. Built-in functions: `min`, `max`, `len`

These three appear constantly and do exactly what their names say.

```python
max(3, 7)          # 7
min(3, 7)          # 3
max(0, end - start + 1)   # the larger of 0 or the window length
len([10, 20, 30])  # 3
```

`max` and `min` can also take a list:

```python
max([1, 5, 2])     # 5
```

**Where you'll see this:** Every example updates a running best with
`max_length = max(max_length, current_length)`. Container With Most Water uses
`min(height[left], height[right])` to find the shorter of two walls.

---

## 9. Sorting a list

`list.sort()` rearranges a list in ascending order *in place* (modifies the
original):

```python
nums = [3, 1, 4, 1, 5]
nums.sort()
# nums is now [1, 1, 3, 4, 5]
```

After sorting, equal values are always next to each other — that's the key
property 3Sum relies on to skip duplicates cheaply.

**Where you'll see this:** `nums.sort()` is the very first step in 3Sum, before
any pointer logic.

> **Ladder note.** `.sort()` mutating the list *in place* is the mutable-sequence
> behaviour drilled in `MutableDemo` ([`../exercises.py`](../exercises.py)). A
> `frozen` value object like `Vector2` could not offer it — mutability is exactly
> the property that makes in-place sorting possible.

---

## 10. Functions and the `self` pattern

A function groups reusable code under a name. You define it with `def` and call
it by name:

```python
def add(a, b):
    return a + b

add(3, 4)    # 7
```

In the examples, functions live inside a `class Solution` and take `self` as
their first parameter. `self` just refers to the object the method belongs to —
you can ignore it for now and focus on the parameters that come after it:

```python
class Solution:
    def twoSum(self, nums, target):
        # nums and target are the real inputs
        ...
```

When LeetCode calls `twoSum`, it passes the list and the target; `self` is
handled automatically.

> **Ladder note.** This is the first sight of `class` and `self`. The full story —
> what `self` binds to, how `__init__`/`__repr__`/`__eq__`/`__hash__` customise an
> object — is the OOP ceiling demonstrated in
> [`../exercises.py`](../exercises.py) (`Vector2`, `MiniSequence`). Here you only
> need to read past `self`; there you implement it.

---

## Putting it together: annotated Two Sum

Here is the simplest example from the pattern doc, with every line explained
using the concepts above:

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        seen = {}                          # empty dictionary (section 3)

        for index, num in enumerate(nums): # loop with index + value (section 5)

            complement = target - num      # arithmetic → the partner we need

            if complement in seen:         # dictionary membership check (section 3)
                return [seen[complement], index]  # early return (section 7)

            seen[num] = index              # store this number's index for later
```

Once you're comfortable with each of those lines individually, the pattern doc's
explanation of *why* the algorithm works will make complete sense.
