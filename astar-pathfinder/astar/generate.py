"""Random map generation."""

import random

from astar.grid import Grid


def random_grid(width, height, density=0.25, seed=None):
    """Build a grid with randomly placed walls.

    density: chance each cell becomes a wall, 0.0 to 1.0
    seed: same seed gives the same map every time
    """
    rng = random.Random(seed)

    start = (0, height // 2)
    goal = (width - 1, height // 2)

    walls = set()
    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if pos == start or pos == goal:
                continue
            if rng.random() < density:
                walls.add(pos)

    return Grid(width, height, walls), start, goal