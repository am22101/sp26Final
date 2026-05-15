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
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
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
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    return [spawn] + list(relics)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    if not graph or source not in graph:
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
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    dist_table = {}
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
    """
    relics_visited_order = []
    minimum_fuel_cost = [float('inf')]
    best_route = []
    relics_visited = dict.fromkeys(relics, False)
    _explore(dist_table, spawn, relics, relics_visited, relics_visited_order,
             0.0, exit_node, best_route, minimum_fuel_cost)

    return (minimum_fuel_cost[0], best_route)


def _explore(dist_table, current_loc, relics, relics_visited, relics_visited_order,
             cost_so_far, exit_node, best, best_cost):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics: list[node]
    relics_remaining : dict[node, bool]
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.
    best_cost : list
        Mutable singleton container for the cost of the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    
    # Pruning condition is safe because it prunes only when it has achieved a greater cost before 
    # even accounting for the cost of the edge to reach the exit. Even in the best case scenario, 
    # (edge weight is 0 to exit), it is still a worse solution than we have found.
    if cost_so_far >= best_cost[0]:
        return
    
    # Possible solution
    if all(relics_visited.values()):
        exit_cost = dist_table[current_loc][exit_node]

        if exit_cost == float('inf'):
            return
        
        total_cost = cost_so_far + exit_cost

        if total_cost < best_cost[0]:
            best_cost[0] = total_cost
            best[:] = relics_visited_order[:]

        return

    for relic_chamber in relics:
        # Visited check
        if relics_visited[relic_chamber]:
            continue

        new_cost = cost_so_far + dist_table[current_loc][relic_chamber]
        if new_cost == float('inf'):
            continue

        relics_visited[relic_chamber] = True
        relics_visited_order.append(relic_chamber)
        _explore(dist_table, relic_chamber, relics, relics_visited, relics_visited_order, 
                 new_cost, exit_node, best, best_cost)
        
        # Backtrack after returning from the above call
        relics_visited_order.pop()
        relics_visited[relic_chamber] = False
    return



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
    """
    # Malformed Argument
    if not graph or spawn not in graph or not relics or exit_node not in graph:
        return (float('inf'), [])
    distance_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(distance_table, spawn, relics, exit_node)



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
