"""A* search over a Grid.

The search runs to completion and records an event log as it goes. The
renderer replays that log afterwards to animate it, so the algorithm
itself stays a plain uninterrupted loop.
"""

import heapq
import time

from astar.heuristics import manhattan


class SearchResult:
    def __init__(self, path, cost, expanded, events, elapsed):
        self.path = path          # list of positions, start -> goal, or [] if none
        self.cost = cost          # total cost of that path, or None
        self.expanded = expanded  # how many nodes came off the queue
        self.events = events      # replay log: ("open", pos) / ("close", pos)
        self.elapsed = elapsed    # seconds


def find_path(grid, start, goal, heuristic=manhattan):
    started_at = time.perf_counter()

    # g[pos] = cheapest known cost from start to pos.
    # A position missing from this dict has not been reached yet, which
    # stands in for "infinity".
    g = {start: 0}

    # came_from[pos] = the position we arrived from. Used to rebuild the path.
    came_from = {start: None}

    closed = set()
    events = []
    expanded = 0

    # The open set. heapq is a min-heap, so entries are (f, counter, position)
    # and the smallest f pops first. The counter breaks ties deterministically
    # and stops Python ever comparing two position tuples when f values match.
    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    events.append(("open", start))

    while open_set:
        _, _, current = heapq.heappop(open_set)

        # A position can be pushed more than once, because we push again
        # every time we find a cheaper route to it. heapq has no
        # decrease-key, so stale copies stay in the heap and we skip them
        # when they surface. The first pop of a position is the good one.
        if current in closed:
            continue

        closed.add(current)
        expanded += 1
        events.append(("close", current))

        if current == goal:
            break

        for neighbour in grid.neighbours(current):
            if neighbour in closed:
                continue

            tentative_g = g[current] + grid.cost(current, neighbour)

            # Accept this route only if it beats the best we know.
            # Strict < is what keeps the final path optimal.
            if neighbour not in g or tentative_g < g[neighbour]:
                g[neighbour] = tentative_g
                came_from[neighbour] = current
                f = tentative_g + heuristic(neighbour, goal)
                counter += 1
                heapq.heappush(open_set, (f, counter, neighbour))
                events.append(("open", neighbour))

    elapsed = time.perf_counter() - started_at

    if goal in closed:
        path = reconstruct(came_from, goal)
        return SearchResult(path, g[goal], expanded, events, elapsed)
    return SearchResult([], None, expanded, events, elapsed)


def reconstruct(came_from, goal):
    """Walk the came_from chain backwards from the goal, then flip it."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path