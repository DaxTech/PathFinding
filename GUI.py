#! python3
"""GUI. Allow user to set the walls."""

import pygame
from HELPER import *

WIDTH = 640
HEIGHT = 640
EXTRA = 100
DIVIDER = 80
GRID_WIDTH = 8
GRID_HEIGHT = 8

SCREEN = pygame.display.set_mode((WIDTH+EXTRA, HEIGHT))
pygame.display.set_caption('PathFinder')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0,  255)

CENTER_A = (WIDTH+EXTRA//2, HEIGHT//4)
CENTER_B = (WIDTH+EXTRA//2, HEIGHT//2+HEIGHT//4)
RADIUS = 40
INSIDE_RADIUS = DIVIDER//2

class Game():
	def __init__(self):
		self.grid = self.grid_setup()
		self.algorithm = DFS()
		self.path = None
		self.starting_point = None
		self.locked = False
		self.grid_after = self.grid
		self.grid_before = self.grid

	def grid_setup(self):
		grid = [[Free((i, j)) for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
		# grid[0][0] = A((0, 0))
		# grid[GRID_HEIGHT-1][GRID_WIDTH-1] = B((GRID_HEIGHT-1, GRID_WIDTH-1))

		return grid

	def find_node(self, value):
		for i in range(GRID_HEIGHT):
			for j in range(GRID_WIDTH):
				if self.grid[i][j].value == value:
					return self.grid[i][j]

	def validate(self):
		counts = 0
		for i in range(GRID_HEIGHT):
			for j in range(GRID_WIDTH):
				if type(self.grid[i][j]) == A:
					counts += 1
				if type(self.grid[i][j]) == B: 
					counts += 1
		if not counts == 2:
			return False
		return True 

	def update_grid(self, coordinates, element):
		x, y = self.get_screen_pos(coordinates)
		x1, y1 = self.get_grid_pos(x, y)
		if element.lower() == 'wall':
			if type(self.grid[y1][x1]) == Free:
				self.grid[y1][x1] = Wall((y1, x1))
				#pygame.draw.rect(SCREEN, WHITE, (x, y, DIVIDER, DIVIDER))
		elif element.lower() == 'free':
			if not type(self.grid[y1][x1]) == Free:
				self.grid[y1][x1] = Free((y1, x1))
				#pygame.draw.rect(SCREEN, BLACK, (x, y, DIVIDER, DIVIDER))
		elif element.lower() == 'a':
			a = self.find_node(1)
			if a is not None:
				y2, x2 = a.pos
				self.grid[y2][x2] = Free((y2, x2))
			if type(self.grid[y1][x1]) == Free:
				self.grid[y1][x1] = A((y1, x1))
		elif element.lower() == 'b':
			b = self.find_node(2)
			if b is not None:
				y2, x2 = b.pos
				self.grid[y2][x2] = Free((y2, x2))
			if type(self.grid[y1][x1]) == Free:
				self.grid[y1][x1] = B((y1, x1))
		#pygame.display.flip()

	def draw_screen(self):
		for i in range(GRID_HEIGHT):
			for j in range(GRID_WIDTH):
				x, y = j * DIVIDER, i * DIVIDER
				if self.grid[i][j].value == 0:
					pygame.draw.rect(SCREEN, BLACK, (x, y, DIVIDER, DIVIDER))
				if self.path and (i, j) in self.path:
					print('HELLO THERE')
					pygame.draw.rect(SCREEN, RED, (x, y, DIVIDER, DIVIDER))
				if self.grid[i][j].value == -1:
					pygame.draw.rect(SCREEN, WHITE, (x, y, DIVIDER, DIVIDER))
				if self.grid[i][j].value == 1:
					pygame.draw.circle(SCREEN, BLUE, (x+INSIDE_RADIUS, y+INSIDE_RADIUS), INSIDE_RADIUS)
				if self.grid[i][j].value == 2:
					pygame.draw.circle(SCREEN, GREEN, (x+INSIDE_RADIUS, y+INSIDE_RADIUS), INSIDE_RADIUS)
		self.drawing_tool()
		pygame.display.flip()

	def clear_screen(self):
		self.grid = [[Free((i, j)) for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

	def get_screen_pos(self, coordinates):
		x, y = coordinates
		return x//DIVIDER*DIVIDER, y//DIVIDER*DIVIDER

	def get_grid_pos(self, x, y):
		return x//DIVIDER, y//DIVIDER

	def print_grid(self):
		for i in range(GRID_HEIGHT):
			for j in range(GRID_WIDTH):
				print(self.grid[i][j].value, end='|')
			print()
		print()

	def drawing_tool(self):
		pygame.draw.rect(SCREEN, BLACK, (WIDTH, 0, EXTRA, HEIGHT))
		pygame.draw.circle(SCREEN, BLUE, CENTER_A,
		   					RADIUS)
		pygame.draw.circle(SCREEN, GREEN, CENTER_B,
						   RADIUS)		
		pygame.display.flip()

	def selected(self, coordinates):
		# Top-left corners:
		ax, ay = CENTER_A[0] - RADIUS, CENTER_A[1] - RADIUS
		bx, by = CENTER_B[0] - RADIUS, CENTER_B[1] - RADIUS
		circle_area_A = [(j, i) for i in range(ay, ay+RADIUS*2+1) for j in range(ax, ax+RADIUS*2+1)]
		circle_area_B = [(j, i) for i in range(by, by+RADIUS*2+1) for j in range(bx, bx+RADIUS*2+1)]	

		if coordinates in circle_area_A:
			return 1
		if coordinates in circle_area_B:
			return 2
		return 0

	def move_point(self, point):
		quit = False
		if point == 0:
			return
		else:
			color = BLUE if point == 1 else GREEN
			update = 'A' if point == 1 else 'B'
			running = True
			while running:
				self.draw_screen()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						quit = True
						running = False
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							running = False
				if pygame.mouse.get_pressed()[0]:
					cords = self.get_screen_pos(pygame.mouse.get_pos())
					if not cords[0] >= WIDTH:
						self.update_grid(cords, update)
				if pygame.mouse.get_pressed()[2]:
					cords = self.get_screen_pos(pygame.mouse.get_pos())
					if not cords[0] >= WIDTH:
						self.update_grid(cords, 'free')
			if quit:
				pygame.quit()
				exit()
			return


	def main_loop(self):
		running = True
		while running:
			self.draw_screen()
			if self.locked:
				if not self.validate():
					self.locked = False
					continue
				self.starting_point = self.find_node(1)
				self.algorithm.path_finder(self.starting_point, self.grid)
				self.path = self.algorithm.reformat_path()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.locked = True
					if event.key == pygame.K_BACKSPACE:
						self.clear_screen()
			if pygame.mouse.get_pressed()[0]:
				cords = pygame.mouse.get_pos()
				if not cords[0] >= WIDTH:
					self.update_grid(cords, 'wall')
				else:
					self.move_point(self.selected(cords))
			if pygame.mouse.get_pressed()[2]:
				cords = pygame.mouse.get_pos()
				if not cords[0] >= WIDTH:
					self.update_grid(cords, 'free')
		pygame.quit()


class DFS:
	def __init__(self):
		self.path = []

	def path_finder(self, node, board):
		node.visited = True  # Avoid cycles.
		if node.value == 2:  # Goal reached.
			return True
		for y, x in node.neighbors:
			# No need to analyze this node.
			if type(board[y][x]) == Wall or board[y][x].visited:
				continue
			# Recursion.
			if self.path_finder(board[y][x], board):
				self.path.append((y, x))
				return True
		return False

	def reformat_path(self):
		self.path.reverse()
		return self.path


if __name__ == '__main__':
	run = Game()
	print(SCREEN.get_width(), SCREEN.get_height())
	run.main_loop()

