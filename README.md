# A* Pathfinder

An animated A* pathfinding tool for the terminal. It finds the shortest path
across a grid map, animates the search as it spreads, and can compare
heuristics side by side on the same map.

Built for Advanced Algorithms, Programming Assignment 1 (Track B).

## Requirements

- Python 3.8 or newer. No third-party packages are needed to run the tool.
- A terminal that supports ANSI colours (Windows Terminal, macOS Terminal,
  and most Linux terminals do).
- `pytest`, only if you want to run the tests: `pip install pytest`

## Running it

 The project lives in the `astar-pathfinder` folder. Run everything from there:

       cd astar-pathfinder

```
python cli.py                              random map, manhattan heuristic, animated
python cli.py --seed 1                     the same map every time
python cli.py --seed 1 --heuristic zero    same map, zero heuristic (Dijkstra)
python cli.py --seed 1 --compare           every heuristic on one map, as a table
python cli.py --map maps/simple.txt        load a map from a file
python cli.py --help                       all options
```

Every random run prints its seed, so any map can be reproduced with `--seed`.

### Options

| Flag | Default | Meaning |
|---|---|---|
| `--map FILE` | | Load a map file instead of generating one |
| `--width N` | 40 | Random map width in cells |
| `--height N` | 12 | Random map height in cells |
| `--density D` | 0.25 | Chance each cell is a wall, 0.0 to 1.0 |
| `--seed N` | random | Seed for map generation |
| `--heuristic H` | manhattan | `manhattan`, `euclidean`, `zero`, or `over` |
| `--compare` | | Run every heuristic on the same map and print a table |
| `--no-animate` | | Print only the final frame |
| `--delay S` | 0.02 | Seconds between animation frames |
| `--steps N` | 5 | Search events per frame; higher is faster |

The animation redraws in place, so the whole map must fit in the terminal
window. If it doesn't, the tool prints the final frame instead and says why.

### Heuristics

- `manhattan`: steps needed on an empty grid. Admissible for 4-way movement.
- `euclidean`: straight-line distance. Admissible, but a weaker estimate.
- `zero`: no estimate at all. A* with this heuristic is Dijkstra's algorithm.
- `over`: manhattan x 3. Deliberately inadmissible, to show what breaks: it
  expands very few cells but can return a longer path.

## Map file format

Plain text, one character per cell:

- `#` wall
- `S` start (exactly one)
- `G` goal (exactly one)
- anything else is open floor

```
S....
.###.
.....
.###.
....G
```

## Colours

| Colour | Meaning |
|---|---|
| Green `S` / red `G` | Start and goal |
| Grey | Wall |
| Light blue | Open set: discovered, not yet expanded |
| Dark blue | Closed: expanded |
| Orange | Final path |

## Project layout

```
astar/
  grid.py         Grid class, neighbours, map file parsing
  heuristics.py   the four heuristics
  search.py       A* itself
  render.py       ANSI rendering and animation replay
  generate.py     random map generation
cli.py            command-line interface
maps/             example map files
tests/            pytest tests
docs/             report
```

## Tests

```
python -m pytest
```

Use `python -m pytest` rather than `pytest`, so the project root is on the
import path.