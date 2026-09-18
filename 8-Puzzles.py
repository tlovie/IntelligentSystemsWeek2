from Algorithms import *
class EightPuzzleProblem(Problem):
    """
    8-puzzle state representation:
      - state is a tuple of length 9 (row-major)
      - 0 represents the blank

    Example:
      (1, 2, 3,
       4, 0, 5,
       6, 7, 8)
    """

    def __init__(self, start, goal):
        super().__init__(start)
        self.goal = goal

    def is_goal(self, state):
        return state == self.goal

    def next_states(self, state):
        blank = state.index(0)          # figure out where the 0 is
        row, col = divmod(blank, 3)     # the row and column of the 0

        moves = []
        if col > 0:                     # if the column is not left most
            moves.append(("L", -1))     # allow a move from the left
        if col < 2:                     # if the column is not right most
            moves.append(("R", 1))      # allow a move from the right
        if row > 0:                     # if the row is not top most
            moves.append(("U", -3))     # allow a move from the top
        if row < 2:                     # if the row is not bottom most
            moves.append(("D", 3))      # allow a move from the bottom


        result = []                     # after we have the moves list need to figure out the layout after move
        for action, delta in moves:
            new_state = list(state)     # state is a tuple - convert that to a list for easier manipulation
            new_blank = blank + delta   # position of new blank simply moves by delta
            new_state[blank], new_state[new_blank] = (  # updates new_state[blank] = new_state[new_blank]
                new_state[new_blank],                   # and     new_state[new_blank] = new_state[blank]
                new_state[blank],                       # in a one-liner tuple syntax
            )
            result.append((action, tuple(new_state)))   # and append the tuple(new_state) to the next_states

        return result


if __name__ == "__main__":
    start = (
        1, 2, 3,
        4, 6, 8,
        7, 5, 0
    )

    goal = (
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    )

    problem = EightPuzzleProblem(start, goal)

    print("\nDFS")
    dfs(problem)

    print("\nBFS")
    bfs(problem)

    print("\nIDDFS")
    iddfs(problem)

