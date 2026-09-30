"""The map: dimensions, walls, and which moves are legal.
 
A position is a tuple (x, y). x is the column, y is the row.
(0, 0) is the top-left corner.
"""
 
# Right, left, down, up. Add the four diagonals here if you ever want
# 8-way movement -- nothing else in this file needs to change.
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
 
 
class Grid:
    def __init__(self, width, height, walls=None):
        self.width = width
        self.height = height
        # A set, not a list: `pos in self.walls` is O(1) and gets called
        # constantly during the search.
        self.walls = set(walls) if walls else set()
 
    def in_bounds(self, position):
        """Is this position on the map at all? Walls are not considered here."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
 
    def passable(self, position):
        """Can we stand on this position?"""
        return position not in self.walls
 
    def neighbours(self, position):
        """The positions reachable in one move from `position`."""
        x, y = position
        result = []
        for dx, dy in DIRECTIONS:
            candidate = (x + dx, y + dy)
            if self.in_bounds(candidate) and self.passable(candidate):
                result.append(candidate)
        return result
 
    def cost(self, from_position, to_position):
        """Cost of one move. Uniform for now -- every step costs 1.
 
        This exists as a method so that weighted terrain (mud = 5, road = 1)
        is a change here and nowhere else.
        """
        return 1
 
 
def parse(text):
    """Build a Grid from a text map.
 
    '#' is a wall, 'S' is the start, 'G' is the goal, anything else is open.
    Returns (grid, start, goal).
    """
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("map is empty")
 
    height = len(lines)
    width = max(len(line) for line in lines)
 
    walls = set()
    start = None
    goal = None
 
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
            elif char == "S":
                start = (x, y)
            elif char == "G":
                goal = (x, y)
 
    if start is None:
        raise ValueError("map has no start 'S'")
    if goal is None:
        raise ValueError("map has no goal 'G'")
 
    return Grid(width, height, walls), start, goal