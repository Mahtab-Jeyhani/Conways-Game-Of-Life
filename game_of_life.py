import pygame

# creating a pygame widow
WIDTH = 720
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Game of Life")
TOTAL_ROWS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255,255)

pygame.init()
clock = pygame.time.Clock()
FPS = 8


class Cell:
	def __init__(self, row, col, width):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.width = width
		self.color = BLACK
		self.alive_neighbors = []

	def make_alive(self):
		self.color = WHITE

	def make_dead(self):
		self.color = BLACK

	def is_alive(self):
		return self.color == WHITE

	def is_dead(self):
		return self.color == BLACK

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.alive_neighbors = []

		# down
		if self.row < TOTAL_ROWS - 1 and grid[self.row + 1][self.col].is_alive():
			self.alive_neighbors.append(grid[self.row + 1][self.col])

		# up
		if self.row > 0 and grid[self.row - 1][self.col].is_alive():
			self.alive_neighbors.append(grid[self.row - 1][self.col])
	
		# left
		if self.col < TOTAL_ROWS - 1 and grid[self.row][self.col + 1].is_alive():
			self.alive_neighbors.append(grid[self.row][self.col + 1])

		# right
		if self.col > 0 and grid[self.row][self.col - 1].is_alive():
			self.alive_neighbors.append(grid[self.row][self.col - 1])

		# upper left corner
		if self.row > 0 and self.col > 0 and grid[self.row-1][self.col-1].is_alive():
			self.alive_neighbors.append(grid[self.row-1][self.col-1])

		# upper right corner
		if self.row > 0 and self.col < TOTAL_ROWS-1 and grid[self.row-1][self.col+1].is_alive():
			self.alive_neighbors.append(grid[self.row-1][self.col+1])

		# lower left corner
		if self.row < TOTAL_ROWS-1 and self.col > 0 and grid[self.row+1][self.col-1].is_alive():
			self.alive_neighbors.append(grid[self.row+1][self.col-1])

		# lower right corner
		if self.row < TOTAL_ROWS-1 and self.col < TOTAL_ROWS-1 and grid[self.row+1][self.col+1].is_alive():
			self.alive_neighbors.append(grid[self.row+1][self.col+1])


def make_grid(width):
	grid = []
	gap = width // TOTAL_ROWS
	grid = [[Cell(i, j, gap) for j in range(TOTAL_ROWS)] for i in range(TOTAL_ROWS)]
	return grid


def draw(win, grid, width):
	win.fill(BLACK)

	# draw cells
	for row in grid:
		for cell in row:
			cell.draw(win)

	pygame.display.update() # update the game window


def get_clicked_position(pos, width):
	gap = width // TOTAL_ROWS # the width of each cell
	y, x = pos # mouse position

	row = y // gap
	col = x // gap

	return row, col # returning the row and column that was clicked


def update_cells(grid, fps):
	cells_to_kill = []
	living_cells = []

	for row in range(TOTAL_ROWS):
		for col in range(TOTAL_ROWS):
			cell = grid[row][col]
			cell.update_neighbors(grid)

			# NEW LIFE - cell with three neighbors comes alive
			if len(cell.alive_neighbors) == 3 and cell.is_dead:
				living_cells.append(cell)
			# OVERPOPULATION - a cell with four or more neighbors dies
			if len(cell.alive_neighbors) > 3:
				cells_to_kill.append(cell)
			# SOLITUDE - a cell with one or no neighbors dies
			if len(cell.alive_neighbors) < 2:
				cells_to_kill.append(cell)
			# HARMONY - a cell with two or three neighbors survives

	for cell in cells_to_kill:
		cell.make_dead()
	for cell in living_cells:
		cell.make_alive()

	clock.tick(fps)


def main(win, width, fps):
	space_count = 0
	grid = make_grid(width)

	run = True
	while run:
		draw(win, grid, width)
		if space_count % 2 != 0:
			update_cells(grid, fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # if we left-click:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, width)
				cell = grid[row][col]
				cell.make_alive()

			elif pygame.mouse.get_pressed()[2]: # if we right-click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, width)
				cell = grid[row][col]
				cell.make_dead()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					space_count += 1

				if event.key == pygame.K_c:
					grid = make_grid(width)
					if space_count % 2 != 0:
						space_count += 1
					for row in range(TOTAL_ROWS):
						for col in range(TOTAL_ROWS):
							cell = grid[row][col]
							cell.make_dead()


if __name__ == '__main__':
	main(WIN, WIDTH, FPS)
