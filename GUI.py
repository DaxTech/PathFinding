#! python3
"""GUI. Allow user to set the walls."""

import pygame
from HELPER import *
from copy import deepcopy
import random

WIDTH = 640
HEIGHT = 640
EXTRA = 100
DIVIDER = 40
GRID_WIDTH = 16
GRID_HEIGHT = 16

CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WIDTH+EXTRA, HEIGHT))
pygame.display.set_caption('PathFinder')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0,  255)
PINK = (255, 105, 180)
CYAN = (0, 200, 200)

CENTER_A = (WIDTH+EXTRA//2, HEIGHT//4)
CENTER_B = (WIDTH+EXTRA//2, HEIGHT//2+HEIGHT//4)
RADIUS = 40
INSIDE_RADIUS = DIVIDER//2

class Game():
	def __init__(self):
		self.grid = self.grid_setup()
		self.algorithm = PathFinder()
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
					if self.grid[i][j].visited:
						pygame.draw.rect(SCREEN, CYAN, (x, y, DIVIDER, DIVIDER))
					else:
						pygame.draw.rect(SCREEN, BLACK, (x, y, DIVIDER, DIVIDER))
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

	def display_path(self):
		if not self.path:
			return
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
			for y, x in self.path:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						exit()
				pygame.time.delay(30)
				y, x = y*DIVIDER, x*DIVIDER
				self.draw_screen()
				path_rect = pygame.Rect(x, y, DIVIDER, DIVIDER)
				pygame.draw.rect(SCREEN, RED, path_rect)
				pygame.display.flip()

	def main_loop(self):
		running = True
		while running:
			self.draw_screen()
			if self.locked:
				if not self.validate():
					self.locked = False
					continue
				self.starting_point = self.find_node(1)
				self.path = self.algorithm.DFS(self.starting_point, self.grid)
				if self.path == False:
					running = False
					break
				if self.path is None:
					raise Exception('No path found')
				del self.path[-1]
				del self.path[0]
				self.display_path()
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


# Important, comment out the PathFinder.draw_nodes() lines and the 
# pygame.event handler loop if you're running this on a text-based version.
class PathFinder:

	@staticmethod
	def draw_nodes(coordinates, color):
		CLOCK.tick(60)  # frames per second (FPS)
		y, x = coordinates
		y, x = y * DIVIDER, x * DIVIDER
		node_rect = pygame.Rect(x, y, DIVIDER, DIVIDER)
		pygame.draw.rect(SCREEN, color, node_rect)
		pygame.display.flip()

	@staticmethod
	def BFS(start_node, board):
		queue = [start_node]  # creates main queue with starting node.
		for node in queue:  
			# Handles pygame events to avoid "Not responding" errors.
			for event in pygame.event.get():  
				if event.type == pygame.QUIT:
					return False
			if node.visited:  # skips visited nodes.
				continue
			node.visited = True
			if node.value == 2:
				return PathFinder.find_path(node, board)  # Formats the path.
			queue += PathFinder.enqueue(node, board)  # Adds children to the queue.
			if node is not start_node:  # Visualization of the process.
				PathFinder.draw_nodes(node.pos, CYAN)
		return None

	@staticmethod
	def DFS(node, board, path=[0], skipped=False):
		if node.value == 2:
			return path
		# Handles pygame events to avoid "Not responding" errors.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:  # The user quitted.
				return False
			if event.type == pygame.KEYDOWN:
				# The user skips the visualization.
				if event.key == pygame.K_SPACE:
					skipped = True
		node.visited = True
		for y, x in node.neighbors:
			if board[y][x].value == -1 or board[y][x].visited:
				continue
			if board[y][x].value == 2:
				return path
			if not skipped and not type(node) == A:
				PathFinder.draw_nodes(node.pos, CYAN)
			results = PathFinder.DFS(board[y][x], board, path, skipped=skipped)
			if results == False:
				return False
			if  results is not None:
				path.insert(0, board[y][x].pos)
				return path
			if not skipped:
				PathFinder.draw_nodes(node.pos, BLACK)
		#node.visited = False
		return None

	@staticmethod
	def enqueue(node, board):
		children = []
		for y, x in node.neighbors:
			if board[y][x].value == -1 or board[y][x].visited:
				continue
			else:
				board[y][x].parent = node
				children.append(board[y][x])
		return children

	@staticmethod
	def find_path(node, board):
		path = [node.pos]
		while True:
			parent = node.parent
			if parent is None:
				break
			path.append(parent.pos)
			node = parent
		path.reverse()
		return path



if __name__ == '__main__':
	run = Game()
	run.main_loop()
