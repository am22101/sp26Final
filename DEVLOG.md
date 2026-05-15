# Development Log – The Torchbearer

**Student Name:** Aidan McSweeney
**Student ID:** 129940054

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [5/6/26]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

The only thing I am certain I should implement right now is finding the shortest path between all interlocations in M. I will implement this first using multiple runs of Dijkstra's on each location given in M and the start location S and tabulate the results of each run similarly to what was shown in ASSIGNMENT.md. I expect the most difficult part will be the computation of the optimal route, as it could get quite costly on time complexity if I do not bound each iteration properly.

---

## Entry 2 – [5/9/26]: Dijkstra's Implementation

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

I implemented Dijkstra's Algorithm with a similar structure to the pseudocode given in the Graphs Quiz. It includes the optimization found in the pseudocode given which prunes any explorations along paths to a node we've already computed a better route to. Instead of returning just a list of values, it returns a dict containing the node keys and their respective shortest time to reach from the source node. This will be run multiple times before we can compute the optimal route.

---

## Entry 3 – [5/13/26]: Search Setup

I finished most of the README documentation regarding algorithm correctness and why a greedy approach would fail finding the optimal route from the shortest paths given by multiple runs of Dijsktra's. I also implemented the short function that creates the 2d table from running Dijkstra's on all the source nodes. I plan to implement the search algorithm next after finalizing the state and search space in the README.

---

## Entry 4 – [5/14/26]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

Some bugs I ran into while doing the final implementation was incorrectlly calling "all" on a dict instead of on their keys, which had unintended side effects. I also forgot to account for a lot of cases when the dist may be inf, which led to some issues when computing and comparing, which would incorrectly result the best route as inf. There was also an indentation bug where I was undoing the backtrack inside of the loop instead of outside of it.

Going into the problem, I had spent a lot of time thinking about how this would differ from the graph problems we had in Assignment 7. Initially, this seemed kind of similar to it, and I was going to implement it like the graph coloring problem, but the more I looked into the question and did a lot of manual tracing on paper (The problem analysis time estimate is probably lowballing it), I figured out this is a search over orders rather than a simple backtracking task. I was originally going to forbid travelling to previously visited required nodes, but that caused issues on my example graphs where some required nodes needed backtracking through previously visited required nodes, which would cause the algorithm to prematurely stop before reaching an actual solution. My solution was then to not prevent revisits entirely, but only to prevent them in the current order. This allowed me to be able to backtrack when necessary, but avoid infinite recursion as well.

If given more time, I would have liked to add predecessor tracking into my Dijkstra's implementation to be able to compute the whole route (not just the order of required cities). I looked into more advanced statistical pruning methods, but they seemed to be incredibly specific to whatever scenario they were being solved for, and backed up with data for the scenario. This simple problem doesn't really require that or have the data, so I decided to just stick with the rudimentary cost pruning method.

---

## Final Entry – [5/14/26]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 6 |
| Part 2: Precomputation Design | 3 |
| Part 3: Algorithm Correctness | 1 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 1 |
| Part 6: Pruning | 0.5 |
| Part 7: Implementation | 4 |
| README and DEVLOG writing | 2 |
| **Total** | 18 |
