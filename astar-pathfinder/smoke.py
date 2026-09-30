from astar.generate import random_grid
from astar.search import find_path
from astar.heuristics import HEURISTICS
from astar.render import animate

grid, start, goal = random_grid(40, 12, density=0.25, seed=1)

manhattan_result = find_path(grid, start, goal, HEURISTICS["manhattan"])
zero_result = find_path(grid, start, goal, HEURISTICS["zero"])

animate(grid, start, goal, manhattan_result, delay=0.02, steps=5)

print("manhattan  cost:", manhattan_result.cost, " expanded:", manhattan_result.expanded)
print("zero       cost:", zero_result.cost, " expanded:", zero_result.expanded)