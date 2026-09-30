"""Command-line entry point: animated A* pathfinding in the terminal.

Examples:
    python cli.py                               random map, manhattan, animated
    python cli.py --seed 1 --heuristic zero     same map every time, Dijkstra
    python cli.py --map maps/simple.txt         load a map file
    python cli.py --seed 1 --compare            every heuristic on one map
"""

import argparse
import random
import shutil
import sys

from astar.generate import random_grid
from astar.grid import parse
from astar.heuristics import HEURISTICS
from astar.render import animate, render
from astar.search import find_path


def build_parser():
    parser = argparse.ArgumentParser(
        description="Animated A* pathfinding in the terminal.",
    )

    source = parser.add_argument_group("map source (random unless --map is given)")
    source.add_argument("--map", metavar="FILE",
                        help="load a map file: '#' wall, 'S' start, 'G' goal")
    source.add_argument("--width", type=int, default=40,
                        help="random map width in cells (default 40)")
    source.add_argument("--height", type=int, default=12,
                        help="random map height in cells (default 12)")
    source.add_argument("--density", type=float, default=0.25,
                        help="chance each cell is a wall, 0.0-1.0 (default 0.25)")
    source.add_argument("--seed", type=int,
                        help="random seed; the same seed always gives the same map")

    search = parser.add_argument_group("search")
    search.add_argument("--heuristic", choices=list(HEURISTICS), default="manhattan",
                        help="heuristic to use (default manhattan; 'zero' is Dijkstra)")
    search.add_argument("--compare", action="store_true",
                        help="run every heuristic on the same map and print a table")

    display = parser.add_argument_group("display")
    display.add_argument("--no-animate", action="store_true",
                         help="skip the animation and print only the final frame")
    display.add_argument("--delay", type=float, default=0.02,
                         help="seconds between frames (default 0.02)")
    display.add_argument("--steps", type=int, default=5,
                         help="search events per frame; higher is faster (default 5)")
    return parser


def validate(parser, args):
    if args.map is None:
        if args.width < 2 or args.height < 1:
            parser.error("--width must be at least 2 and --height at least 1")
        if not 0.0 <= args.density <= 1.0:
            parser.error("--density must be between 0.0 and 1.0")
    if args.steps < 1:
        parser.error("--steps must be at least 1")
    if args.delay < 0:
        parser.error("--delay cannot be negative")


def load_map(parser, args):
    """Return (grid, start, goal, description)."""
    if args.map:
        try:
            with open(args.map) as f:
                grid, start, goal = parse(f.read())
        except FileNotFoundError:
            parser.error(f"map file not found: {args.map}")
        except ValueError as e:
            parser.error(f"invalid map file {args.map}: {e}")
        return grid, start, goal, args.map

    # Pick a seed even when none was given, and report it, so any run
    # can be reproduced exactly.
    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    grid, start, goal = random_grid(args.width, args.height, args.density, seed)
    desc = f"random {args.width}x{args.height}, density {args.density}, seed {seed}"
    return grid, start, goal, desc


def closed_cells(result):
    return {pos for kind, pos in result.events if kind == "close"}


def fits_terminal(grid):
    """The animation redraws in place, which only works if the whole
    frame fits on screen. Leave a few rows for the stats underneath."""
    columns, rows = shutil.get_terminal_size()
    return grid.width * 2 <= columns and grid.height + 4 <= rows


def run_compare(grid, start, goal, desc):
    # Zero heuristic is Dijkstra, which is always optimal: use it as the
    # reference to flag any heuristic that returned a longer path.
    optimal = find_path(grid, start, goal, HEURISTICS["zero"]).cost

    print(f"map: {desc}")
    print()
    print(f"{'heuristic':<12}{'cost':>6}{'expanded':>10}{'time (ms)':>12}  optimal?")
    print("-" * 50)
    for name, h in HEURISTICS.items():
        r = find_path(grid, start, goal, h)
        cost = "-" if r.cost is None else f"{r.cost:g}"
        if r.cost is None:
            verdict = "no path"
        elif r.cost == optimal:
            verdict = "yes"
        else:
            verdict = f"NO (+{r.cost - optimal:g})"
        print(f"{name:<12}{cost:>6}{r.expanded:>10}{r.elapsed * 1000:>12.2f}  {verdict}")


def run_single(args, grid, start, goal, desc):
    result = find_path(grid, start, goal, HEURISTICS[args.heuristic])

    animate_it = not args.no_animate
    if animate_it and not fits_terminal(grid):
        print("Map is larger than the terminal window, so animation would "
              "scroll. Showing the final frame only (enlarge the window, or "
              "use a smaller --width/--height, to animate).", file=sys.stderr)
        animate_it = False

    if animate_it:
        animate(grid, start, goal, result, delay=args.delay, steps=args.steps)
    else:
        print(render(grid, start, goal, closed_cells(result), set(), result.path))

    print(f"map: {desc}")
    print(f"heuristic: {args.heuristic}")
    if result.cost is None:
        print(f"no path exists  (expanded {result.expanded} cells)")
    else:
        print(f"cost: {result.cost:g}  expanded: {result.expanded}  "
              f"time: {result.elapsed * 1000:.2f} ms")


def main():
    parser = build_parser()
    args = parser.parse_args()
    validate(parser, args)
    grid, start, goal, desc = load_map(parser, args)

    if args.compare:
        run_compare(grid, start, goal, desc)
    else:
        run_single(args, grid, start, goal, desc)


if __name__ == "__main__":
    main()