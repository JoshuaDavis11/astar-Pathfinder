from astar.grid import Grid, parse
from astar.search import find_path
from astar.heuristics import HEURISTICS
from astar.generate import random_grid


def assert_valid_path(grid, start, goal, path):
    """Every step must be a legal move: adjacent and not a wall."""
    assert path[0] == start
    assert path[-1] == goal
    for a, b in zip(path, path[1:]):
        assert b in grid.neighbours(a), f"illegal step {a} -> {b}"


def test_simple_map_finds_shortest_path():
    grid, start, goal = parse("S....\n.###.\n.....\n.###.\n....G")
    result = find_path(grid, start, goal)
    assert result.cost == 8
    assert_valid_path(grid, start, goal, result.path)


def test_no_path_returns_empty():
    grid, start, goal = parse("S#.\n##.\n..G")
    result = find_path(grid, start, goal)
    assert result.path == []
    assert result.cost is None


def test_start_equals_goal():
    grid = Grid(3, 3)
    result = find_path(grid, (1, 1), (1, 1))
    assert result.path == [(1, 1)]
    assert result.cost == 0


def test_manhattan_matches_dijkstra_but_expands_no_more():
    for seed in range(20):
        grid, start, goal = random_grid(40, 12, density=0.25, seed=seed)
        m = find_path(grid, start, goal, HEURISTICS["manhattan"])
        z = find_path(grid, start, goal, HEURISTICS["zero"])
        assert m.cost == z.cost
        assert m.expanded <= z.expanded
        if m.path:
            assert_valid_path(grid, start, goal, m.path)


def test_overestimate_path_is_valid_but_can_be_longer():
    grid, start, goal = random_grid(40, 12, density=0.25, seed=1)
    over = find_path(grid, start, goal, HEURISTICS["over"])
    zero = find_path(grid, start, goal, HEURISTICS["zero"])
    assert_valid_path(grid, start, goal, over.path)
    assert over.cost >= zero.cost