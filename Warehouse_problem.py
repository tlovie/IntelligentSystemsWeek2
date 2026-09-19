from Warehouse_Robot import generate_weighted_warehouse_board
from Algorithms_updated import *

class Warehouse_problem(Problem):

    def __init__( self, grid, start, goal ):
        super().__init__(start)
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])
        for row in grid:
            print(" ".join(f"{v:2d}" for v in row))

    def is_goal(self, state):
        return state == self.goal

    def next_states(self, state):
        row, col = state
        moves = [   ("DN", (row + 1, col)),
                    ("RT", (row, col + 1)),
                    ("LF", (row, col - 1)),
                    ("UP", (row - 1, col)),  ]

        result = []
        for action, (r, c) in moves:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                result.append((action, (r, c)))

        return result

    def g(self, state):
        row, col = state
        return grid[row][col]

    def h(self, state):
        row, col = state
        goal_row, goal_col = self.goal

        return abs(goal_row-row) + abs(goal_col-col)


if __name__ == "__main__":

    board = generate_weighted_warehouse_board(size=8, difficulty="hard", seed=42)
    grid = board["grid"]
    start = board["start"]
    goal = board["goal"]

    problem = Warehouse_problem( grid = grid, start = start, goal = goal )

    print("\nDFS")
    dfs(problem)

    print("\nBFS")
    bfs(problem)

    #print("\nIDDFS")
    #iddfs(problem)

    print("\nUCS")
    ucs(problem)

    print("\nGreedy Best-First Search")
    greedy_best_first(problem)

    print("\nA*")
    astar(problem)