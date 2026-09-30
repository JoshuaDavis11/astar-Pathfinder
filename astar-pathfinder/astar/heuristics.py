"""Heuristics: cheap estimates of the cost from a to b, ignoring walls.

Each is a pure function of two positions. None of them know the grid or
the search exist -- that is the whole point of keeping them here.

A heuristic is *admissible* if it never overestimates the true cost. A*
only guarantees a shortest path when the heuristic is admissible.
"""

import math


def manhattan(a, b):
    """Steps needed on an empty 4-way grid. Admissible for 4-way movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    """Straight-line distance. Admissible, but weaker than manhattan for
    4-way movement: it always returns a smaller number, so it does less
    to steer the search."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def zero(a, b):
    """No estimate at all. A* with this heuristic IS Dijkstra's algorithm."""
    return 0


def overestimate(a, b):
    """Deliberately inadmissible: 3x too large.

    Expands very few nodes, but the path it returns may not be the
    shortest. Included so the tool can demonstrate what admissibility
    is actually protecting.
    """
    return 3 * manhattan(a, b)


# Name -> function, so the CLI can map a --heuristic flag onto one of these.
HEURISTICS = {
    "manhattan": manhattan,
    "euclidean": euclidean,
    "zero": zero,
    "over": overestimate,
}