from collections import deque
import heapq


# -------------------------
# Problem definition
# -------------------------
class Problem:
    def __init__(self, start):
        self.start = start

    def is_goal(self, state):
        raise NotImplementedError

    def next_states(self, state):
        """
        Return list of (action, next_state)
        """
        raise NotImplementedError

    # --- New: cost + heuristic hooks (used by UCS / Greedy / A*) ---
    def g(self, state):
        """
        Step cost to enter `state` (default: 1).
        For unit-cost problems, keep this as 1.
        """
        return 1

    def h(self, state):
        """
        Heuristic estimate from `state` to goal (default: 0).
        """
        return 0


# -------------------------
# Shared path utilities
# -------------------------
def build_path(parent, goal):
    states = []
    actions = []

    s = goal
    while s is not None:
        states.append(s)
        prev, act = parent[s]
        if prev is None:
            break
        actions.append(act)
        s = prev

    states.reverse()
    actions.reverse()
    return states, actions


def print_solution(parent, goal):
    states, actions = build_path(parent, goal)
    print("Goal:", states[-1])
    print("Actions:", actions)
    #print("States:", states)
    print("Steps:", len(actions))


# -------------------------
# Breadth-First Search
# -------------------------
def bfs(problem):
    start = problem.start
    queue = deque([start])
    visited = {start}
    parent = {start: (None, None)}

    while queue:
        state = queue.popleft()

        if problem.is_goal(state):
            print_solution(parent, state)
            return

        for action, nxt in problem.next_states(state):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = (state, action)
            queue.append(nxt)

    print("No solution (BFS)")


# -------------------------
# Depth-First Search (iterative)
# -------------------------
def dfs(problem):
    start = problem.start
    stack = [start]
    visited = {start}
    parent = {start: (None, None)}

    while stack:
        state = stack.pop()

        if problem.is_goal(state):
            print_solution(parent, state)
            return

        for action, nxt in problem.next_states(state):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = (state, action)
            stack.append(nxt)

    print("No solution (DFS)")

# -------------------------
# Depth-Limited Search
# -------------------------
def dls(problem, limit):
    start = problem.start

    parent = {start: (None, None)}
    path = {start}

    status, goal = dls_recursive( problem, start, 0, limit, path, parent )

    return status, parent, goal


def dls_recursive(problem, state, depth, limit, path, parent):

    # Goal test
    if problem.is_goal(state):
        return "found", state

    # We reached the current depth limit
    if depth == limit:
        return "cutoff", None

    cutoff_occurred = False

    for action, nxt in problem.next_states(state):

        # Prevent cycles along the current path
        if nxt in path:
            continue

        # Descend into this branch
        path.add(nxt)
        parent[nxt] = (state, action)

        status, goal = dls_recursive( problem, nxt, depth + 1, limit, path, parent )

        if status == "found":
            return "found", goal

        if status == "cutoff":
            cutoff_occurred = True

        # Backtrack
        path.remove(nxt)
        del parent[nxt]

    if cutoff_occurred:
        return "cutoff", None

    return "failure", None


# -------------------------
# Iterative Deepening DFS
# -------------------------
def iddfs(problem):
    depth = 0

    while True:
        status, parent, goal = dls(problem, depth)

        if status == "found":
            print("Found at depth:", depth)
            print_solution(parent, goal)
            return

        if status == "failure":
            print("No solution (IDDFS)")
            return

        depth += 1

# -------------------------
# Uniform-Cost Search (UCS)
# -------------------------
def ucs(problem):
    start = problem.start

    # (path_cost, tie_breaker, state)
    heap = []
    heapq.heappush(heap, (0,  start))

    parent = {start: (None, None)}
    best_cost = {start: 0}

    while heap:
        cost,state = heapq.heappop(heap)

        # Skip stale entries
        if cost != best_cost.get(state, None):
            continue

        if problem.is_goal(state):
            print("Cost:", cost)
            print_solution(parent, state)
            return

        for action, nxt in problem.next_states(state):
            new_cost = cost + problem.g(nxt)

            if new_cost < best_cost.get(nxt, float("inf")):
                best_cost[nxt] = new_cost
                parent[nxt] = (state, action)
                heapq.heappush(heap, (new_cost, nxt))

    print("No solution (UCS)")


# -------------------------
# Greedy Best-First Search
# -------------------------
def greedy_best_first(problem):
    start = problem.start

    # (heuristic, tie_breaker, state)
    heap = []
    heapq.heappush(heap, (problem.h(start),  start))

    parent = {start: (None, None)}
    visited = {start}

    while heap:
        _, state = heapq.heappop(heap)

        if problem.is_goal(state):
            print_solution(parent, state)
            return

        for action, nxt in problem.next_states(state):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = (state, action)
            heapq.heappush(heap, (problem.h(nxt),  nxt))

    print("No solution (Greedy Best-First)")


# -------------------------
# A* Search
# -------------------------
def astar(problem):
    start = problem.start

    # (f = g+h, tie_breaker, state)
    heap = []


    g_cost = {start: 0}
    heapq.heappush(heap, (problem.h(start),  start))

    parent = {start: (None, None)}

    while heap:
        f, state = heapq.heappop(heap)

        # Skip stale entries
        if f != g_cost.get(state, float("inf")) + problem.h(state):
            continue

        if problem.is_goal(state):
            print("Cost:", g_cost[state])
            print_solution(parent, state)
            return

        for action, nxt in problem.next_states(state):
            tentative_g = g_cost[state] + problem.g(nxt)

            if tentative_g < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = tentative_g
                parent[nxt] = (state, action)
                heapq.heappush(heap, (tentative_g + problem.h(nxt),  nxt))

    print("No solution (A*)")
