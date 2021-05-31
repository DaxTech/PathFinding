import pygame
import time
import sys
import math
from HELPER import *

CLOCK = pygame.time.Clock()
pygame.init()


class Algorithms:
    def __init__(self, screen, maze, source, name, div, color, destination=None):
        self.screen = screen
        self.maze = maze
        self.source = source
        self.name = name
        self.div = div
        self.color = color
        self.destination = destination
        self.path = []

    def execute(self):
        if self.name.lower() == "bfs":
            result = self.bfs()
            del result[-1]
            return result
        elif self.name.lower() == "dfs":
            result = self.dfs(self.source, self.maze)
            del result[0]
            del result[-1]
            return result
        elif self.name.lower() == "a*":
            return

    def bfs(self):
        queue = [self.source]
        for node in queue:
            if node.visited:
                continue
            node.visited = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
            if node.value == 2:
                return self.find_path(node)
            queue += Algorithms.enqueue(node, self.maze)
            if node.value == 0:
                self.highlight(node.x, node.y)

    def dfs(self, node, board):
        if node.value == 2:
            self.path.insert(0, node)
            return self.path
        node.visited = True
        for y, x in node.get_neighbors():
            if board[y][x].visited or (board[y][x].is_wall and not board[y][x].value == 2):
                continue
            if node.value == 2:
                self.path.insert(0, node)
                return self.path
            if node.value == 0:
                self.highlight(node.x, node.y)
            success = self.dfs(board[y][x], board)
            if success:
                self.path.insert(0, node)
                return self.path
        self.highlight(node.x, node.y, color=(0, 0, 0))
        return None

    @staticmethod
    def enqueue(node, maze):
        children = []
        for y, x in node.get_neighbors():
            if maze[y][x].visited or (maze[y][x].is_wall and maze[y][x].value == 0):
                continue
            else:
                maze[y][x].parent = node
                children.append(maze[y][x])
        return children

    def highlight(self, x, y, color=None):
        color = self.color if not color else color
        CLOCK.tick(60)
        pygame.draw.rect(self.screen, color, (x * self.div, y * self.div, self.div, self.div))
        pygame.display.flip()

    def find_path(self, node):
        path = [node]
        while True:
            parent = node.parent
            if parent is self.source:
                break
            path.append(parent)
            node = parent
        path.reverse()
        return path

    #def a_star(self):
        #path = [self.source]
        #for node in path:
