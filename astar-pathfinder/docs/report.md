# PA1 Report — A* Pathfinding

## (a) What I built
- Algorithm: A* search on a 2D grid, 4-way movement, every step costs 1
- Language: Python — why?
- Cells stored as (x, y) tuples — why?
- Package layout: grid / heuristics / search / render / generate — why split?
- Open set: heapq with stale entries skipped (no decrease-key)
- Event log recorded during search, replayed for animation
- Terminal (ANSI colours) instead of a GUI — why? (cross-platform, WinForms Windows-only)
- Simplifications: no diagonals, no weighted terrain

## (b) The tool
- What it does:
- How A* sits inside it:
- Interface decisions: (CLI flags — fill in once built)
- Worked example: (paste a run + screenshot later)

## (c) What I learned
- 5x5 simple map: manhattan and zero BOTH expanded all 19 cells — heuristic gave no benefit. Why?
- 40x20 seed 1: manhattan 172 vs zero 560 expanded, same cost 45
- 40x12 seed 1: manhattan 159 vs zero 321 expanded, same cost 47
- Paths that LOOKED blocked but were valid — fixed with colour, verified via cost arithmetic
- Frames stacking when grid taller than terminal
- Other surprises:

## (d) AI use
- Tools used + roughly how much:
- What for:
- Where the AI was wrong / unhelpful:
  - Gave a file layout, then wrote code that didn't follow it (heuristics in search.py) — I caught it
  - Did it again with the parse() function in grid.py
  - Video search returned aggregator sites, not real YouTube links
  - Smoke test written for a flat layout after giving a package layout
- What I understood vs took on trust: