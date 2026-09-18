from Algorithms import *


class GridPath(Problem):
    def __init__(self, grid, start, goal):
        super().__init__(start)
        self.grid = grid
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_goal(self, state):
        return state == self.goal

    def next_states(self, state):
        row, col = state
        moves = [   ("UP", (row - 1, col)),
                    ("DOWN", (row + 1, col)),
                    ("LEFT", (row, col - 1)),
                    ("RIGHT", (row, col + 1)),  ]

        result = []
        for action, (r, c) in moves:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] == 0:
                    result.append((action, (r, c)))

        return result


grid = [
    [0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0]
]

p = GridPath(grid, start=(0, 0), goal=(2, 4))
print("\nBFS")
bfs(p)

print("\nDFS")
dfs(p)

print("\nIDDFS")
iddfs(p)