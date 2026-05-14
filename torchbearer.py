"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Aidan McSweeney
Student ID:   129940054

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return """
    Why a single shortest-path run from S is not enough:
    The objective of the torchbearer is to go from S to T while visiting every relic location in M, not just going from S to T.
    What decision remains after all inter-location costs are known:
    The decision still remains to choose the shortest path that visits every location in M starting at S and ending at T.
    Why this requires a search over orders (one sentence):
    Every potential solution must have some order of the locations in M, and we must search through them to find the cheapest path.
    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    return relics.append(spawn)


def run_dijkstra(graph, source):
    if not graph or not source:
        return
    value = dict.fromkeys(graph, float('inf'))
    value[source] = 0
    pq = []
    heapq.heappush(pq, (value[source], source))
    
    while pq:
        (current_value, current_node) = heapq.heappop(pq)

        if current_value > value[current_node]:
            continue

        for (adjacent_node, weight) in graph[current_node]:
            if value[current_node] + weight < value[adjacent_node]:
                value[adjacent_node] = value[current_node] + weight
                heapq.heappush(pq, (value[adjacent_node], adjacent_node))        
    return value


def precompute_distances(graph, spawn, relics, exit_node):
    if not graph or not spawn or not relics or not exit_node:
        return
    dist_table = dict()
    sources = select_sources(spawn, relics, exit_node)
    for current_node in sources:
        dist_table[current_node] = run_dijkstra(graph, current_node)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return """
    What the Invariant Means For nodes already finalized (in S):
    Distance recorded is the true shortest path.
    What the Invariant Means For nodes not yet finalized (not in S):
    Distance recorded is the shortest path so far made up nodes who all have a true shortest path to them.
    Initialization: 
    Before the first iteration, all nodes are undiscovered except for the start node. The true shortest path from any node to itself is 0, and the undiscovered node paths are all initialized to infinity because they have not been visited.  
    Maintenance: 
    When the algorithm chooses edges to explore, it always chooses them in order of increasing cost. When a node is finalized, it is visited via choosing the least expensive edge possible from that point. Since all weights are non-negative, there is no way a future choice would beat the path that uses the cheapest edge to that node.
    Termination: 
    Since the algorithm terminates only when all possible to reach nodes have been visited, every node will be finalized and thus be in S. Therefore, the algorithm finds the true shortest path from the source to all reachable nodes.
    Why This Matters for the Route Planner:
    From the goal statement, we must find the shortest path from S to T visiting all M nodes, which requires finding the correct shortest path from any of these nodes to one another.
    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    return """
    The failure mode: Not visiting every relic chamber before reaching the exit
    Counter-example setup:
        G = (
            S: (B, 2), (C, 4)
            B: (T, 1)
            C: (B, 2), (T, 3)
            T: 
            )   
        M = (B, C)
    What greedy picks: Greedy will choose the cheapest edge, SB
    What optimal picks: Optimal chooses SC, because its the only way to visit all relic chambers.
    Why greedy loses: Greedy has now chosen a path where the only edge avaliable leads to the exit, but it still hasn't visited all relic chambers yet.
    What the Algorithm Must Explore: The algorithm must explore optimal orders of the relic chambers.
    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
