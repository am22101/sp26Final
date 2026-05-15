# The Torchbearer

**Student Name:** Aidan McSweeney
**Student ID:** 129940054
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  The objective of the torchbearer is to go from S to T while visiting every relic location in M, not just going from S to T.

- **What decision remains after all inter-location costs are known:**
  The decision still remains to choose the shortest path that visits every location in M starting at S and ending at T.

- **Why this requires a search over orders (one sentence):**
  Every potential solution must have some order of the locations in M, and we must search through them to find the cheapest path.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Start Nodes | Needed to get anywhere since its the only place to start. |
| Relic Nodes | Need to know shortest paths from relics since we need to visit them all. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Dict |
| What the keys represent | Vertices |
| What the values represent | Edges |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Hashing |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k + 1
- **Cost per run:** (n + m)logn operations per run
- **Total complexity:** (k) * (n + m)logn total operations
- **Justification (one line):** We perform n binary heap operations that each cost logn, and run the algorithm on m edges a total of k + 1 times because there are k relic chambers and 1 start node.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  Distance recorded is the true shortest path.

- **For nodes not yet finalized (not in S):**
  Distance recorded is the shortest path so far made up nodes who all have a true shortest path to them.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  Before the first iteration, all nodes are undiscovered except for the start node. The true shortest path from any node to itself is 0, and the undiscovered node paths are all initialized to infinity because they have not been visited.  

- **Maintenance : why finalizing the min-dist node is always correct:**
  When the algorithm chooses edges to explore, it always chooses them in order of increasing cost. When a node is finalized, it is visited via choosing the least expensive edge possible from that point. Since all weights are non-negative, there is no way a future choice would beat the path that uses the cheapest edge to that node.

- **Termination : what the invariant guarantees when the algorithm ends:**
  Since the algorithm terminates only when all possible to reach nodes have been visited, every node will be finalized and thus be in S. Therefore, the algorithm finds the true shortest path from the source to all reachable nodes.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

From the goal statement, we must find the shortest path from S to T visiting all M nodes, which requires finding the correct shortest path from any of these nodes to one another.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Not visiting every relic chamber before reaching the exit
- **Counter-example setup:** Take the following graph:
G = (
  S: (B, 2), (C, 4)
  B: (T, 1)
  C: (B, 2), (T, 3)
  T: 
)

and list of relic chambers:

M = (B, C)
- **What greedy picks:** Greedy will choose the cheapest edge, SB
- **What optimal picks:** Optimal chooses SC, because its the only way to visit all relic chambers.
- **Why greedy loses:** Greedy has now chosen a path where the only edge avaliable leads to the exit, but it still hasn't visited all relic chambers yet.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must search over orders of the relic chambers

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | current chamber being explored |
| Relics already collected | relics_remaining | dict | how many relic chambers have been visited |
| Fuel cost so far | cost_so_far | float | total cost of edge weights traversed |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | dict (hashmap) |
| Operation: check if relic already collected | Time complexity: O(1) with good hashing |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | Because this problem requires a lot of lookups and updates, hashmaps provide O(1) average for both. |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** O(k!)
- **Why:** Because each node is distinct, there are k! possible ways to order the list of nodes.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** cost_so_far
- **When it is used:** pruning and determining best solutions
- **What it allows the algorithm to skip:** paths that cost more or equal to the best path already found.

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** The current node, order, and cost so far
- **What the lower bound accounts for:** It accounts for all nonnegative edge values, even 0
- **Why it never overestimates:** It can never overestimate because it only includes costs already travelled.

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- Pruning is safe because there are no negative weight edges, which means the lower bound estimation is always less than or equal to the true optimal cost. 

---

## References

> Bullet list. If none beyond lecture notes, write that.

- I used the Graphs Practice Quiz pseudocode as reference for building my Dijkstra's Algorithm implementation. 
