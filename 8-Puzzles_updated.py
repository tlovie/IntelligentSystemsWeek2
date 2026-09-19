from Algorithms_updated import *


class EightPuzzleProblem(Problem):
    """
    8-puzzle state representation:
      - state is a tuple of length 9 (row-major)
      - 0 represents the blank
    """

    def __init__(self, start, goal):
        super().__init__(start)
        self.goal = goal
        # Pre-compute goal positions for fast Manhattan distance
        self.goal_pos = {}
        for i, tile in enumerate(goal):
            self.goal_pos[tile] = divmod(i, 3)


    def is_goal(self, state):
        return state == self.goal

    def next_states(self, state):
        blank = state.index(0)
        row, col = divmod(blank, 3)

        moves = []
        if col > 0:
            moves.append(("L", -1))
        if col < 2:
            moves.append(("R", 1))
        if row > 0:
            moves.append(("U", -3))
        if row < 2:
            moves.append(("D", 3))

        result = []
        for action, delta in moves:
            new_blank = blank + delta
            new_state = list(state)
            new_state[blank], new_state[new_blank] = (
                new_state[new_blank],
                new_state[blank],
            )
            result.append((action, tuple(new_state)))

        return result

    # --- New hooks for UCS / Greedy / A* ---
    def g(self, state):
        # Unit step cost: each move costs 1
        return 1

    def h(self, state):
        # Manhattan distance (sum over tiles 1..8; ignore blank 0)
        dist = 0
        for i, tile in enumerate(state):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = self.goal_pos[tile]
            dist += abs(r - gr) + abs(c - gc)
        return dist


if __name__ == "__main__":
    start = (
        0, 8, 2,
        3, 1, 4,
        7, 6, 5
    )

    goal = (
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    )

    problem = EightPuzzleProblem(start, goal)

    print("\nBFS")
    bfs(problem)

    print("\nDFS")
    dfs(problem)

    print("\nIDDFS")
    iddfs(problem)

    print("\nUCS")
    ucs(problem)

    print("\nGreedy Best-First Search")
    greedy_best_first(problem)

    print("\nA*")
    astar(problem)
