"""Depth-first-search algorithm. The shortest path is not assured."""

class Node:
    def __init__(self, position, value=0, free=False, width=9, height=9):
        # Each node starts with an y, x position in the grid,
        # without any edges.
        self.y, self.x = position
        self.value = value
        self.width = width
        self.height = height
        # Edges defined: [North: bool, West: bool, South: bool, East: bool]
        if free:
            self.edges = [False for i in range(4)]
        else:
            self.edges = [True for i in range(4)]
        self.visited = False
        self.parent = None

    def get_neighbors(self):
        neighbors = []
        north, west, south, east = self.edges
        # Gets neighbor position depending if there are edges to either direction
        if not north and not self.y-1 < 0:
            neighbors.append((self.y-1, self.x))
        if not west and not self.x-1 < 0:
            neighbors.append((self.y, self.x-1))
        if not south and not self.y+1 > HEIGHT-1:
            neighbors.append((self.y+1, self.x))
        if not east and not self.x+1 > WIDTH-1:
            neighbors.append((self.y, self.x+1))
        return neighbors

    def unchecked_neighbors(self):
        neighbors = []
        if not self.y-1 < 0:
            neighbors.append((self.y-1, self.x))
        if not self.y+1 > self.height-1:
            neighbors.append((self.y+1, self.x))
        if not self.x+1 > self.width-1:
            neighbors.append((self.y, self.x+1))
        if not self.x-1 < 0:
            neighbors.append((self.y, self.x-1))
        return neighbors

class Cell:
    def __init__(self, position, value=0, is_wall=False, width=9, height=9):
        self.y, self.x = position
        self.value = value
        self.width = width
        self.height = height
        self.is_wall = is_wall
        self.visited = False

    def get_neighbors(self):
        neighbors = []
        if not self.y-1 < 0:
            neighbors.append((self.y-1, self.x))
        if not self.y+1 > self.height-1:
            neighbors.append((self.y+1, self.x))
        if not self.x+1 > self.width-1:
            neighbors.append((self.y, self.x+1))
        if not self.x-1 < 0:
            neighbors.append((self.y, self.x-1))
        return neighbors
