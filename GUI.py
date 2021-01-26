"""GUI and visualization."""

import pygame
import sys
import os
from HELPER import *
from MAZES import *

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 200, 200)

GREENISH = (149, 242, 101)
YELLOW = (255, 237, 18)
ORANGE = (255, 124, 0)

WIDTH, HEIGHT = 730, 630
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Images:
RAT = pygame.image.load(os.path.join('.', 'rat2.png'))  # big
CHEESE = pygame.image.load(os.path.join('.', 'cheese.png'))  # big

class Game:
    def __init__(self, height=21, width=21, cwidth=11, cheight=11,div=30):
        # cwidth & cheight account for what the size of maze the computer will be using to create the mazes.
        self.width, self.height = width, height
        self.cwidth, self.cheight = cwidth, cheight
        self.div = div
        self.maze = None
        self.font = pygame.font.SysFont('DoppioOne-Regular.ttf', 72)

    def get_pos(self, coordinates):
        x, y = coordinates
        return x//self.div*self.div, y//self.div*self.div

    def get_grid_pos(self, coordinates):
        x, y = coordinates
        return y//self.div, x//self.div

    def update_grid(self, coordinates, wall=False):
        i, j = self.get_grid_pos(coordinates)
        x, y = self.get_pos(coordinates)
        rect_area = pygame.Rect(x, y, self.div, self.div)
        color = GREENISH if not wall else BLACK
        self.maze[i][j].is_wall = False if not wall else True
        pygame.draw.rect(SCREEN, color, rect_area)
        pygame.display.flip()

    def draw(self):
        for row in self.maze:
            for cell in row:
                CLOCK.tick(60)
                self.mouse_pressed()
                event_handler()
                x, y  = cell.x*self.div, cell.y*self.div
                cell_area = pygame.Rect(x, y, self.div, self.div)
                if not cell.is_wall:
                    pygame.draw.rect(SCREEN, GREENISH, cell_area)
                else:
                    pygame.draw.rect(SCREEN, BLACK, cell_area)
                pygame.display.flip()

    def mouse_pressed(self):
        # Drawing onto the screen.
        if pygame.mouse.get_pressed()[0]: # left mouse button pressed.
            position = pygame.mouse.get_pos()
            self.update_grid(position)
        if pygame.mouse.get_pressed()[2]: # right button pressed.
            position = pygame.mouse.get_pos()
            self.update_grid(position, wall=True)

    def main_loop(self):
        SCREEN.fill(BLACK)
        pygame.display.flip()
        running = True
        #self.maze = binary_tree(self.cwidth, self.cheight)
        self.maze = dfs_generator(self.cwidth, self.cheight)
        #self.maze = [[Cell((i, j), is_wall=True, width=2*self.width-1, height=2*self.height-1) for j in range(2*self.width-1)] for i in range(2*self.height-1)]
        while running:
            CLOCK.tick(60)
            self.draw()
            # Event handling.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.mouse_pressed()
        pygame.quit()
        sys.exit(1)

    def menu_helper(self):
        SCREEN.fill(BLACK)
        title = self.font.render('A RAT IN A MAZE', 1, WHITE)  # Length: 418px Height: 72px
        change_size = self.font.render('GRID SIZE', 1, WHITE)  # Length 255 Height: 72px
        play = self.font.render('PLAY', 1, WHITE)  # Length: 128px Height: 72px
        SCREEN.blit(title, (156, 28))
        SCREEN.blit(play, (301, 418))
        SCREEN.blit(change_size, (237, 518))
        SCREEN.blit(RAT, (172, 100))
        SCREEN.blit(CHEESE, (428, 100))
        pygame.draw.rect(SCREEN, WHITE, (291, 408, 148, 75), width=3)
        pygame.draw.rect(SCREEN, WHITE, (227, 508, 275, 75), width=3)
        pygame.display.flip()

    def grid_options(self):
        # MAZE SIZES: 9x9 (5x5) DIV: 70, 15x15 (8x8) DIV: 42, 21x21 (11x11) DIV: 30, 63x63 (32x32) DIV:10
        SCREEN.fill(BLACK)
        messages = [
        'SELECT GRID SIZE:',
        'SMALL(9X9)',
        'MEDIUM(15x15)',
        'LARGE(21x21)',
        'EXTRA LARGE(63x63)',
        ]
        areas = []
        colors = [WHITE, GREENISH, YELLOW, ORANGE, RED]
        for msg, color in zip(messages, colors):
            text = self.font.render(msg, 1, color)
            x, y = text.get_size()
            x_pos = (WIDTH - x) // 2
            y_pos = 28 + 100*messages.index(msg)
            if not messages.index(msg) == 0:
                pygame.draw.rect(SCREEN, color, (x_pos-10, y_pos-10, x+20, y+20), width=3)
                area = [(j, i) for j in range(x_pos, x_pos+x+20) for i in range(y_pos, y_pos+y+20)]
                areas.append(area)
            SCREEN.blit(text, (x_pos, y_pos))
        pygame.display.flip()
        return areas

    def apply_changes(self, size):
        if size.lower() == "small":
            self.width, self.height = 9, 9
            self.cwidth, self.cheight = 5, 5
            self.div = 70
        elif size.lower() == "medium":
            self.width, self.height = 15, 15
            self.cwidth, self.cheight = 8, 8
            self.div = 42
        elif size.lower() == "large":
            self.width, self.height = 21, 21
            self.cwidth, self.cheight = 11, 11
            self.div = 30
        elif size.lower() == "extra large":
            self.width, self.height = 63, 63
            self.cwidth, self.cheight = 32, 32
            self.div = 10
        return

    def grid_menu(self):
        selection_areas = self.grid_options()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos in selection_areas[0]:  # small
                        self.apply_changes('small')
                        running = False
                    if event.pos in selection_areas[1]:  # medium
                        self.apply_changes('medium')
                        running = False
                    if event.pos in selection_areas[2]:  # large
                        self.apply_changes('large')
                        running = False
                    if event.pos in selection_areas[3]:  # extra large
                        self.apply_changes('extra large')
                        running = False
        return



    def main_menu(self):
        play_area = [(x, y) for x in range(291, 291+148) for y in range(408, 408+75)]
        size_area = [(x, y) for x in range(227, 227+275) for y in range(508, 508+75)]
        running = True
        while running:
            self.menu_helper()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos in play_area:
                        self.main_loop()
                    if event.pos in size_area:
                        self.grid_menu()

if __name__ == "__main__":
    pygame.init()
    run = Game()
    run.main_menu()
