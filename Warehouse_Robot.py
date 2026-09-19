import random
from typing import List, Tuple, Dict, Union, Optional


def generate_weighted_warehouse_board(
    size: int,
    difficulty: Union[str, int] = "easy",
    seed: Optional[int] = None,
) -> Dict[str, object]:
    """
    Generate an initial board for a Warehouse Robot pathfinding problem with weighted terrain.

    Board model:
      - grid[r][c] is an integer cost to ENTER that cell (>= 1).
      - start and goal are (row, col) tuples.
      - difficulty increases by assigning higher weights to more cells and/or higher max weights.

    Returns:
      {
        "grid": 2D list of ints,
        "start": (r, c),
        "goal": (r, c),
        "size": int,
        "difficulty": normalized difficulty name
      }

    Notes for search:
      - Use step cost = grid[next_r][next_c]
      - A simple admissible heuristic for A*: Manhattan distance * min_cell_cost (which is 1 here).
    """
    if size < 2:
        raise ValueError("size must be >= 2")

    rng = random.Random(seed)

    # Normalize difficulty into parameters
    # density: fraction of cells (excluding a guaranteed path) that become heavier
    # wmax: maximum weight assigned to heavy cells
    if isinstance(difficulty, int):
        # Map 1..5 to difficulty
        lvl = max(1, min(5, difficulty))
        diff_name = ["easy", "medium", "hard", "very_hard", "extreme"][lvl - 1]
    else:
        diff_name = str(difficulty).strip().lower()

    params = {
        "easy":      {"density": 0.10, "wmax": 3},
        "medium":    {"density": 0.20, "wmax": 5},
        "hard":      {"density": 0.30, "wmax": 8},
        "very_hard": {"density": 0.40, "wmax": 12},
        "extreme":   {"density": 0.55, "wmax": 20},
    }
    if diff_name not in params:
        raise ValueError(f"Unknown difficulty: {difficulty}. Use easy/medium/hard/very_hard/extreme or 1..5.")

    density = params[diff_name]["density"]
    wmax = params[diff_name]["wmax"]

    # Base grid: all costs = 1
    grid: List[List[int]] = [[1 for _ in range(size)] for _ in range(size)]
    start = (0, 0)
    goal = (size - 1, size - 1)

    # --- Guarantee at least one "reasonable" path: carve a low-cost path from start to goal ---
    # We'll build a simple random monotone path (only right/down) and keep it cost 1.
    path_cells = set()
    r, c = start
    path_cells.add((r, c))

    moves = ["R"] * (size - 1) + ["D"] * (size - 1)
    rng.shuffle(moves)
    for mv in moves:
        if mv == "R":
            c += 1
        else:
            r += 1
        path_cells.add((r, c))

    # --- Increase weights on some other cells based on difficulty ---
    # Choose candidate cells excluding the guaranteed path, start, goal.
    candidates = [
        (rr, cc)
        for rr in range(size)
        for cc in range(size)
        if (rr, cc) not in path_cells and (rr, cc) != start and (rr, cc) != goal
    ]

    rng.shuffle(candidates)
    heavy_count = int(len(candidates) * density)

    # Assign heavier terrain weights
    # Weight range starts at 2 so we actually make it "heavier" than normal.
    for (rr, cc) in candidates[:heavy_count]:
        grid[rr][cc] = rng.randint(2, wmax)

    # Optionally: add a few "very heavy" hotspots in harder modes to create interesting choices
    if diff_name in {"hard", "very_hard", "extreme"}:
        hotspots = max(1, size // 2)  # small number of hotspots
        hotspot_cells = candidates[heavy_count:heavy_count + hotspots]
        for (rr, cc) in hotspot_cells:
            grid[rr][cc] = wmax  # max penalty

    # Ensure start/goal are low-cost
    grid[start[0]][start[1]] = 1
    grid[goal[0]][goal[1]] = 1

    return {
        "grid": grid,
        "start": start,
        "goal": goal,
        "size": size,
        "difficulty": diff_name,
    }


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    board = generate_weighted_warehouse_board(size=40, difficulty="extreme", seed=42)
    grid, start, goal = board["grid"], board["start"], board["goal"]

    print("Start:", start, "Goal:", goal, "Difficulty:", board["difficulty"])
    for row in grid:
        print(" ".join(f"{v:2d}" for v in row))
