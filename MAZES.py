"""Maze generation algorithms"""

import pygame
import random
import sys
from HELPER import *

HEIGHT, WIDTH = 10, 10

DIV = 30
SCREEN = pygame.display.set_mode((630, 630))
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
CLOCK = pygame.time.Clock()

def binary_tree(width, height):
    maze = [[Node((i, j), width=width, height=width) for j in range(width)] for i in range(height)]
    for i in range(height):
        for j in range(width):
            if i - 1 < 0 and not j - 1 < 0:
                maze[i][j - 1].edges[3] = False
                maze[i][j].edges[1] = False
                continue
            if j - 1 < 0 and not i - 1 < 0:
                maze[i - 1][j].edges[2] = False
                maze[i][j].edges[0] = False
                continue
            if j - 1 < 0 and i - 1 < 0:
                continue
            toss = random.randint(0, 1)
            if toss == 1:
                # Connect North
                maze[i - 1][j].edges[2] = False
                maze[i][j].edges[0] = False
            else:
                # Connect West
                maze[i][j - 1].edges[3] = False
                maze[i][j].edges[1] = False
    return transform(maze, width, height)

def dfs_generator(width, height):
    maze = [[Node((i, j), width=width, height=width) for j in range(width)] for i in range(height)]
    start_node = maze[0][0]
    stack = [start_node]
    while not stack == []:
        node = stack.pop()
        node.visited = True
        neighbors = node.unchecked_neighbors()
        if not neighbors:
            continue
        random.shuffle(neighbors)
        for y, x in neighbors:
            if not maze[y][x].visited:
                chosen = maze[y][x]
                chosen.visited = True
                if chosen.x > node.x:
                    chosen.edges[1] = False
                    node.edges[3] = False
                if chosen.x < node.x:
                    chosen.edges[3] = False
                    node.edges[1] = False
                if chosen.y < node.y:
                    chosen.edges[2] = False
                    node.edges[0] = False
                if chosen.y > node.y:
                    chosen.edges[0] = False
                    node.edges[2] = False
                stack.append(node)
                stack.append(chosen)
                break
    return transform(maze, width, height)

def transform(maze, width, height):
    wid, hei = 2*width-1, 2*height-1
    new_maze = []
    for i in range(hei):
        if not i % 2 == 0:
            row = [Cell((i, x), is_wall=True, width=wid, height=hei) for x in range(wid)]
            new_maze.append(row)
            continue
        row = []
        for j in range(wid):
            if j % 2 == 0:
                row.append(maze[i//2][j//2])
            else:
                row.append(Cell((i, j), is_wall=True, width=wid, height=hei))
        new_maze.append(row)

    for i in range(0, hei, 2):
        for j in range(0, wid, 2):
            if not new_maze[i][j].edges[0]:
                new_maze[i-1][j].is_wall = False
            if not new_maze[i][j].edges[3]:
                new_maze[i][j+1].is_wall = False
            new_maze[i][j] = Cell((i, j), width=wid, height=hei)
    return new_maze

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
def draw(board):
    """Draws transformed maze."""
    for row in board:
        for cell in row:
            CLOCK.tick(60)
            event_handler()
            x, y  = cell.x*DIV, cell.y*DIV
            cell_area = pygame.Rect(x, y, DIV, DIV)
            if not cell.is_wall:
                pygame.draw.rect(SCREEN, RED, cell_area)
                pygame.display.flip()

def sample(board):
    """Draws maze with line-walls instead of cube/cell walls."""
    for row in board:
        for cell in row:
            y, x = cell.y*DIVIDER, cell.x*DIVIDER
            COLOR = BLACK
            pygame.draw.rect(SCREEN, COLOR, (x, y, DIVIDER, DIVIDER))
            north, west, south, east = cell.edges
            if north:
                pygame.draw.line(SCREEN, WHITE, (x, y), (x+DIVIDER, y), width=3)
            if west:
                pygame.draw.line(SCREEN, WHITE, (x, y), (x, y+DIVIDER), width=3)
            if south:
                pygame.draw.line(SCREEN, WHITE, (x, y+DIVIDER), (x+DIVIDER, y+DIVIDER), width=3)
            if east:
                pygame.draw.line(SCREEN, WHITE, (x+DIVIDER, y), (x+DIVIDER, y+DIVIDER), width=3)
            pygame.display.flip()


if __name__ == "__main__":
    uinp = sys.argv[1]
    if uinp.lower() == 'btree':
        MAZE = binary_tree(11, 11)
    elif uinp.lower() == 'dfs':
        MAZE = dfs_generator(11, 11)
    SCREEN.fill(BLACK)
    running = True
    while running:
        draw(MAZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
