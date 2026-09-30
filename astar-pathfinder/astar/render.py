"""Turn a grid and a search state into a printable string."""

RESET = "\033[0m"


def cell(colour, text="  "):
    """Two characters with a coloured background, from the 256-colour palette."""
    return f"\033[48;5;{colour}m{text}{RESET}"


WALL   = cell(240)          # grey
EMPTY  = "  "               # terminal default
OPEN   = cell(67)           # muted blue: discovered
CLOSED = cell(24)           # dark blue: expanded
PATH   = cell(214)          # orange
START  = cell(28, "S ")     # green
GOAL   = cell(160, "G ")    # red

import sys, time

def render(grid, start, goal, closed, open_set, path):
    """Build one frame as a single string.

    closed, open_set: sets of positions
    path: list of positions, or [] while the search is still running
    """
    path_cells = set(path)

    lines = []
    for y in range(grid.height):
        row = []
        for x in range(grid.width):
            pos = (x, y)

            # Order matters. A path cell is also a closed cell, so the
            # path has to be checked first or it never shows.
            if pos in grid.walls:
                row.append(WALL)
            elif pos == start:
                row.append(START)
            elif pos == goal:
                row.append(GOAL)
            elif pos in path_cells:
                row.append(PATH)
            elif pos in closed:
                row.append(CLOSED)
            elif pos in open_set:
                row.append(OPEN)
            else:
                row.append(EMPTY)

        lines.append("".join(row))

    return "\n".join(lines)



HOME = "\033[H"        # move cursor to top-left
CLEAR = "\033[2J"      # clear screen
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

def animate(grid, start, goal, result, delay=0.02, steps=1):
       closed, open_set = set(), set()
       sys.stdout.write(HIDE_CURSOR + CLEAR + HOME)
       try:
           for i, (kind, pos) in enumerate(result.events):
               if kind == "open":
                   open_set.add(pos)
               else:
                   closed.add(pos)
                   open_set.discard(pos)

               if i % steps == 0 or i == len(result.events) - 1:
                   sys.stdout.write(HOME + render(grid, start, goal, closed, open_set, []))
                   sys.stdout.flush()
                   time.sleep(delay)

           sys.stdout.write(HOME + render(grid, start, goal, closed, open_set, result.path))
       finally:
           sys.stdout.write(SHOW_CURSOR + "\n")
           sys.stdout.flush()