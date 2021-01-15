"""Depth-first-search algorithm. The shortest path is not assured."""

WIDTH = 8
HEIGHT = 8

class Node:
    def __init__(self, position):
        self.pos = position
        self.neighbors = self.find_neighbors()
        self.visited = False

    def find_neighbors(self):
        y, x = self.pos
        neighbors = []
        if not y+1 > HEIGHT-1:
            neighbors.append((y+1, x))
        if not y-1 < 0:
            neighbors.append((y-1, x))
        if not x+1 > WIDTH-1:
            neighbors.append((y, x+1))
        if not x-1 < 0:
            neighbors.append((y, x-1))
        return neighbors

class A(Node):
    def __init__(self, position):
        super().__init__(position)
        self.value = 1

class B(Node):
    def __init__(self, position):
        super().__init__(position)
        self.value = 2

class Free(Node):
    def __init__(self, position):
        super().__init__(position)
        self.value = 0
        self.visited = False

class Wall:
    def __init__(self, position):
        self.pos = position
        self.value = -1