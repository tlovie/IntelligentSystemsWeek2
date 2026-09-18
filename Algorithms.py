from collections import deque

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


# -------------------------
# Shared path utilities
# -------------------------
def build_path(parent, goal):
    # this routine builds the path starting from the goal and working backwards.
    states = []         # list that contains all the states
    actions = []        # list that contains all the actions

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
    print("States:", states)


# -------------------------
# Breadth-First Search
# -------------------------
def bfs(problem):
    start = problem.start
    queue = deque([start])          # queue object (deque)
    visited = {start}               # set
    parent = {start: (None, None)}  # dictionary

    while queue:
        state = queue.popleft()

        if problem.is_goal(state):          # if true we have achieved the goal in minimum steps
            print_solution(parent, state)   # output the solution
            return

        for action, nxt in problem.next_states(state):      # problem class must provide this
            if nxt in visited:              # don't revisit any states
                continue                    # that we have already been
            visited.add(nxt)                # now add the candidate state to visisted
            parent[nxt] = (state, action)   # and record the path we took to get here
            queue.append(nxt)               # and queue it for exploration at end of queue.

    print("No solution (BFS)")


# -------------------------
# Depth-First Search (iterative)
# -------------------------
def dfs(problem):
    start = problem.start
    stack = [start]                 # list (can operate as a stack)
    visited = {start}               # set
    parent = {start: (None, None)}  # dictionary

    while stack:
        state = stack.pop()         # creates the current state variable

        if problem.is_goal(state):          # check if we have reached goal
            print_solution(parent, state)   # print solution
            return              

        for action, nxt in problem.next_states(state):  # problem must provide this
            if nxt in visited:              # ensure that we have not already evaluated this
                continue
            visited.add(nxt)                # now add to visited set
            parent[nxt] = (state, action)   # and record path info
            stack.append(nxt)               # add to stack to explore next

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