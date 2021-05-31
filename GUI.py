"""GUI and visualization."""

import pygame
import sys
import os
from HELPER import *
from MAZES import *
from PATHFINDING import *

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
PINK = (255, 0, 242)
LIGHT_GREEN = (0, 255, 148)
LIGHT_BLUE = (0, 173, 255)
PURPLE = (195, 0, 255)

WIDTH, HEIGHT = 930, 630
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Images:
RAT = pygame.image.load(os.path.join('.', 'rat.png'))  # big
CHEESE = pygame.image.load(os.path.join('.', 'cheese.png'))  # big


class Game:
    def __init__(self, height=21, width=21, cwidth=11, cheight=11, div=30):
        # cwidth & cheight account for what the size of maze the computer will be using to create the mazes.
        self.width, self.height = width, height
        self.cwidth, self.cheight = cwidth, cheight
        self.div = div
        self.from_menu = False  # Block mouse_pressed event
        self.slow_down = False  # Decides on the speed of the maze generation visualization
        self.maze = None
        self.rat = pygame.transform.scale(RAT, (div, div))
        self.cheese = pygame.transform.scale(CHEESE, (div, div))
        self.font = pygame.font.SysFont('DoppioOne-Regular.ttf', 72)
        self.algorithm = 'bfs'
        self.source = None
        self.path = None
        self.destination = None

    @staticmethod
    def paint_black():
        SCREEN.fill(BLACK)
        pygame.display.flip()

    def get_pos(self, coordinates):
        x, y = coordinates
        return x // self.div * self.div, y // self.div * self.div

    def get_grid_pos(self, coordinates):
        x, y = coordinates
        return y // self.div, x // self.div

    @staticmethod
    def center(n):
        return (WIDTH - n) // 2

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.outbound_click(event.pos)

    def update_grid(self, coordinates, wall=False, value=0):
        i, j = self.get_grid_pos(coordinates)
        x, y = self.get_pos(coordinates)
        rect_area = pygame.Rect(x, y, self.div, self.div)
        color = BLACK if not wall else WHITE
        if self.maze[i][j].is_wall and not value == 0:
            self.maze[i][j].is_wall = True
        else:
            self.maze[i][j].is_wall = False if not wall else True
        if not value == 0:
            img = False
            for row in self.maze:
                for cell in row:
                    if cell.value == value and not (cell.y, cell.x) == (i, j):
                        img = cell
                        break
            if img:
                img.value = 0
        self.maze[i][j].value = value
        if not value == 0:
            blit_img = self.rat if value == 1 else self.cheese
            pygame.draw.rect(SCREEN, BLACK, rect_area)
            SCREEN.blit(blit_img, (x, y))
            if img:
                color = BLACK if not img.is_wall else WHITE
                pygame.draw.rect(SCREEN, color, (img.x * self.div, img.y * self.div, self.div, self.div))
        else:
            pygame.draw.rect(SCREEN, color, rect_area)
        pygame.display.flip()

    def reset_maze(self):
        self.maze = [
            [Cell((i, j), is_wall=False, width=self.width, height=self.height)
             for j in range(self.width)]
            for i in range(self.height)]
        self.path = []

    def draw(self):
        pygame.draw.rect(SCREEN, WHITE, (630, 0, self.div, HEIGHT))
        self.rat_cheese_selector()
        self.right_buttons(['MAZES', 'PATHS'], [ORANGE, LIGHT_GREEN])
        self.clear_button()
        self.start_button()
        for row in self.maze:
            for cell in row:
                if self.slow_down:
                    CLOCK.tick(120)
                if self.mouse_pressed():
                    return  # cut-off to avoid over-drawing the past maze.
                if self.event_handler():
                    return
                x, y = cell.x * self.div, cell.y * self.div
                cell_area = pygame.Rect(x, y, self.div, self.div)
                if not cell.value == 0:
                    pygame.draw.rect(SCREEN, BLACK, cell_area)
                    blit_img = self.rat if cell.value == 1 else self.cheese
                    SCREEN.blit(blit_img, (x, y))
                else:
                    if not cell.is_wall:
                        if self.path is not None and cell in self.path:
                            pygame.draw.rect(SCREEN, PURPLE, cell_area)
                            self.path_line(cell)
                        else:
                            color = BLACK if not cell.visited else LIGHT_BLUE
                            pygame.draw.rect(SCREEN, color, cell_area)
                    else:
                        pygame.draw.rect(SCREEN, WHITE, cell_area)
                pygame.display.flip()
        self.slow_down = False

    def maze_button(self):
        font = pygame.font.SysFont('DoppioOne-Regular.ttf', 52)
        button = font.render('MAZES', 1, ORANGE)
        screen_left = 630 + self.div
        button_pos = screen_left + (WIDTH - screen_left - button.get_width()) // 2
        SCREEN.blit(button, (button_pos, 38))
        pygame.draw.rect(SCREEN, ORANGE, (button_pos - 10, 28, button.get_width() + 20, 52), width=3)
        area = [(x, y) for x in range(button_pos - 10, button_pos + button.get_width() + 10) for y in range(28, 80)]
        return area

    def right_buttons(self, text, colors):
        font = pygame.font.SysFont('DoppioOne-Regular.ttf', 52)
        areas = []
        screen_left = 630 + self.div
        for msg, color in zip(text, colors):
            message = font.render(msg, 1, color)
            x = screen_left + (WIDTH - screen_left - message.get_width()) // 2
            y = 38 + 100 * text.index(msg)
            SCREEN.blit(message, (x, y))
            pygame.draw.rect(SCREEN, color, (x - 10, y - 10, message.get_width() + 20, message.get_height() + 20),
                             width=3)
            a = [(j, i) for j in range(x - 10, x + message.get_width() + 10) for i in
                 range(y - 10, y + message.get_height() + 10)]
            areas.append(a)
        pygame.display.flip()
        return areas

    def rat_cheese_selector(self):
        areas = []
        rat_img = pygame.transform.scale(RAT, (96, 96))
        cheese_img = pygame.transform.scale(CHEESE, (64, 64))
        screen_left = 630 + self.div
        rat_x = screen_left + (WIDTH - screen_left - 160) // 2
        cheese_x = rat_x + 96  # 10 pixels of difference so they are not too close to each other.
        SCREEN.blit(rat_img, (rat_x - 10, 240))
        SCREEN.blit(cheese_img, (cheese_x, 250))
        pygame.display.flip()
        areas.append([(x, y) for x in range(rat_x - 10, rat_x + 96 - 10) for y in range(240, 240 + 96)])
        areas.append([(x, y) for x in range(cheese_x, cheese_x + 64) for y in range(250, 250 + 64)])
        return areas

    def clear_button(self):
        font = pygame.font.SysFont('GOUDYSTO.ttf', 52, True)
        clear = font.render('CLEAR', 1, BLACK)
        screen_left = 630 + self.div
        x = screen_left + (WIDTH - screen_left - clear.get_width()) // 2
        y = 570
        pygame.draw.rect(SCREEN, RED, (x - 10, y - 10, clear.get_width() + 20, clear.get_height() + 20))
        SCREEN.blit(clear, (x, y))
        area = [(j, i) for j in range(x - 10, x + clear.get_width() + 20) for i in
                range(y - 10, y + clear.get_height() + 20)]
        return area

    def start_button(self):
        start = self.font.render('START', 1, BLACK)
        wid, hei = start.get_width(), start.get_height()
        screen_left = 630 + self.div
        x = screen_left + (WIDTH - screen_left - wid) // 2
        y = 400
        pygame.draw.rect(SCREEN, GREEN, (x - 10, y - 10, wid + 20, hei + 20))
        SCREEN.blit(start, (x, y))
        pygame.display.flip()
        area = [(j, i) for j in range(x - 10, x + wid + 20) for i in range(y - 10, y + hei + 20)]
        return area

    def outbound_click(self, pos):
        right_areas = self.right_buttons(['MAZES', 'PATHS'], [ORANGE, LIGHT_GREEN])
        right_areas += self.rat_cheese_selector()
        right_areas.append(self.clear_button())
        right_areas.append(self.start_button())
        if pos in right_areas[0]:
            self.maze_menu()
        if pos in right_areas[1]:
            self.pathfinding_menu()
        if pos in right_areas[2]:
            self.move_img('rat')
        if pos in right_areas[3]:
            self.move_img('cheese')
        if pos in right_areas[4]:
            self.reset_maze()
        if pos in right_areas[5]:
            self.find_path()
        return True

    def mouse_pressed(self):
        # Drawing onto the screen
        if self.from_menu:
            pygame.event.wait(1500)
            self.from_menu = False
        if pygame.mouse.get_pressed()[0]:  # left mouse button pressed.
            position = pygame.mouse.get_pos()
            if not position[0] >= 630:
                y, x = self.get_grid_pos(position)
                if self.maze[y][x].value == 1:
                    self.move_img('rat')
                elif self.maze[y][x].value == 2:
                    self.move_img('cheese')
                else:
                    self.update_grid(position, wall=True)
        if pygame.mouse.get_pressed()[2]:  # right button pressed.
            position = pygame.mouse.get_pos()
            if not position[0] >= 630:
                self.update_grid(position)
        return

    def move_img(self, img):
        moving = True
        while moving:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    moving = False
                    break
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if not pos[0] >= 630:
                    value = 1 if img.lower() == 'rat' else 2
                    self.update_grid(pos, value=value)
        return

    def main_loop(self):
        self.paint_black()
        running = True
        self.reset_maze()
        while running:
            CLOCK.tick(120)
            self.draw()
            # Event handling.
            self.event_handler()
            self.mouse_pressed()

    def menu_helper(self):
        SCREEN.fill(BLACK)
        title = self.font.render('A RAT IN A MAZE', 1, WHITE)  # Length: 418px Height: 72px
        change_size = self.font.render('GRID SIZE', 1, WHITE)  # Length 255 Height: 72px
        play = self.font.render('PLAY', 1, WHITE)  # Length: 128px Height: 72px
        title_pos = self.center(title.get_width())
        play_pos = self.center(play.get_width())
        size_pos = self.center(change_size.get_width())
        SCREEN.blit(title, (title_pos, 28))
        SCREEN.blit(play, (play_pos, 418))
        SCREEN.blit(change_size, (size_pos, 518))
        # Get rat and cheese position: sum = 256px(rat width) + 128px(cheese width)
        # (WIDTH - sum) // 2
        img_pos = self.center(RAT.get_width() + CHEESE.get_width())
        SCREEN.blit(RAT, (img_pos, 100))
        SCREEN.blit(CHEESE, (img_pos + 256, 100))
        pygame.draw.rect(SCREEN, WHITE, (play_pos - 10, 408, 148, 75), width=3)
        pygame.draw.rect(SCREEN, WHITE, (size_pos - 10, 508, 275, 75), width=3)
        pygame.display.flip()

    def menu_generator(self, messages, colors):
        SCREEN.fill(BLACK)
        areas = []
        for msg, color in zip(messages, colors):
            text = self.font.render(msg, 1, color)
            x, y = text.get_size()
            x_pos = self.center(x)
            y_pos = 28 + 100 * messages.index(msg)
            if not messages.index(msg) == 0:
                pygame.draw.rect(SCREEN, color, (x_pos - 10, y_pos - 10, x + 20, y + 20), width=3)
                area = [(j, i) for j in range(x_pos, x_pos + x + 20) for i in range(y_pos, y_pos + y + 20)]
                areas.append(area)
            SCREEN.blit(text, (x_pos, y_pos))
        pygame.display.flip()
        return areas

    def apply_changes(self, size):
        if size.lower() == "small":
            w, h, cw, ch, d = 9, 9, 5, 5, 70
        elif size.lower() == "medium":
            w, h, cw, ch, d = 15, 15, 8, 8, 42
        elif size.lower() == "large":
            w, h, cw, ch, d = 21, 21, 11, 11, 30
        elif size.lower() == "extra large":
            w, h, cw, ch, d = 63, 63, 32, 32, 10
        self.width, self.height = w, h
        self.cwidth, self.cheight = cw, ch
        self.div = d
        self.rat = pygame.transform.scale(RAT, (d, d))
        self.cheese = pygame.transform.scale(CHEESE, (d, d))
        return

    def grid_menu(self):
        # MAZE SIZES: 9x9 (5x5) DIV: 70, 15x15 (8x8) DIV: 42, 21x21 (11x11) DIV: 30, 63x63 (32x32) DIV:10
        selection_areas = self.menu_generator(
            ['SELECT GRID SIZE', 'SMALL(9X9)', 'MEDIUM(15x15)', 'LARGE(21X21)', 'EXTRA LARGE(63x63)'],
            [WHITE, GREENISH, YELLOW, ORANGE, RED])
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
        self.from_menu = True
        play_area = [(x, y) for x in range(391, 391 + 148) for y in range(408, 408 + 75)]
        size_area = [(x, y) for x in range(327, 327 + 275) for y in range(508, 508 + 75)]
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

    def maze_changes(self, algorithm):
        self.slow_down = True
        SCREEN.fill(BLACK)
        pygame.display.flip()
        if algorithm.lower() == 'dfs':
            self.maze = dfs_generator(self.cwidth, self.cheight)
            return
        elif algorithm.lower() == 'btree':
            self.maze = binary_tree(self.cwidth, self.cheight)
            return

    def maze_menu(self):
        self.from_menu = True
        selected_areas = self.menu_generator(
            ['Pick an algorithm for your maze:', 'Depth-first-search',
             'Binary tree'],
            [WHITE, PINK, LIGHT_GREEN]
        )
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paint_black()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos in selected_areas[0]:
                        self.maze_changes('dfs')
                        return
                    if event.pos in selected_areas[1]:
                        self.maze_changes('btree')
                        return

    def pathfinding_menu(self):
        self.from_menu = True
        selected_areas = self.menu_generator(['Select a path-finding algorithm:',
                                              'Breadth-first-search', 'Depth-first-search', 'A* search'],
                                             [WHITE, LIGHT_GREEN,
                                              PINK, LIGHT_BLUE])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paint_black()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos in selected_areas[0]:
                        self.algorithm = 'bfs'
                        self.paint_black()
                        return
                    if event.pos in selected_areas[1]:
                        self.algorithm = 'dfs'
                        self.paint_black()
                        return
                    if event.pos in selected_areas[2]:
                        self.algorithm = 'a*'
                        self.paint_black()
                        return

    def validate(self):
        counts = 0
        for row in self.maze:
            for cell in row:
                if cell.value == 1:
                    counts += 1
                    self.source = cell
                if cell.value == 2:
                    counts += 1
                    self.destination = cell
        if not counts == 2:
            return False
        return True

    def find_source(self, cell, value):
        # Finds the rat or the cheese, depending on the value passed
        for i, j in cell.get_neighbors():
            if self.maze[i][j].value == 1 and value == 0:
                return self.maze[i][j]
            if self.maze[i][j].value == 2 and value == -1:
                return self.maze[i][j]

    def display_path(self):
        t = 30 if self.height == 9 else 120
        if not self.path:
            return
        for cell in self.path:
            x, y = cell.x * self.div, cell.y * self.div
            CLOCK.tick(t)
            cell_area = pygame.Rect(x, y, self.div, self.div)
            pygame.draw.rect(SCREEN, PURPLE, cell_area)
            pygame.display.flip()
            self.path_line(cell)
        return

    def path_line(self, cell):
        l_width = self.div // 10
        indx = self.path.index(cell)
        x, y = cell.x * self.div, cell.y * self.div
        prev_cell = self.path[indx-1] if not (indx == 0) else self.find_source(cell, 0)
        next_cell = self.path[indx+1] if not (indx == len(self.path)-1) else self.find_source(cell, -1)
        if prev_cell.y == next_cell.y: # draw a horizontal line
            sy = y + self.div //2 - l_width # y pos of line
            pygame.draw.line(SCREEN, GREEN, (x, sy), (x+self.div, sy), width=l_width)
        elif prev_cell.x == next_cell.x: # draw a vertical line
            sx = x + self.div // 2 - l_width # x pos of line 
            pygame.draw.line(SCREEN, GREEN, (sx, y), (sx, y+self.div), width=l_width)
        else: # turn left, right, up or down
            y1 = y+self.div//2-l_width
            x1 = x+self.div//2-l_width
            if next_cell.y > cell.y or prev_cell.y > cell.y:
                y2 = y+self.div
                pygame.draw.line(SCREEN, GREEN, (x1, y1), (x1, y2), width=l_width)
            else:
                pygame.draw.line(SCREEN, GREEN, (x1, y), (x1, y1), width=l_width)
            if prev_cell.x > cell.x or next_cell.x > cell.x:
                x2 = x+self.div
                pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2, y1), width=l_width)
            else:
                pygame.draw.line(SCREEN, GREEN, (x, y1), (x1, y1), width=l_width)    


    def update_maze(self):
        for row in self.maze:
            for cell in row:
                if cell.visited:
                    cell.visited = False

    def find_path(self):
        if not self.validate():
            return
        self.update_maze()
        finder = Algorithms(SCREEN, self.maze, self.source, self.algorithm, self.div, LIGHT_BLUE, self.destination)
        self.path = finder.execute()
        self.display_path()


if __name__ == "__main__":
    pygame.init()
    run = Game()
    run.main_menu()
