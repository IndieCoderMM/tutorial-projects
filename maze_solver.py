import pygame
import sys
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Maze Solver")
ROWS = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (244, 0, 0)
GREEN = (76, 175, 80)
BLUE = (3, 160, 254)
YELLOW = (255, 193, 7)
PURPLE = (170, 0, 255)
GREY = (158, 158, 158)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.color = WHITE

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = YELLOW

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    # def is_open(self):
    #     return self.color == GREEN
    #
    # def is_closed(self):
    #     return self.color == RED

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == YELLOW

    def is_end(self):
        return self.color == BLUE

    def draw_spot(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def show_path(draw, current, came_from, start, end):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        end.make_end()
        start.make_start()
        draw()

def astar_pathfinder(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            show_path(draw, current, came_from, start, end)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

    return False


def make_grid():
    grid = []
    gap = WIDTH // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j, gap, ROWS)
            grid[i].append(spot)
    return grid

def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(WIN, BLACK, (0, i * gap), (WIDTH, i * gap))
        for j in range(ROWS):
            pygame.draw.line(WIN, GREY, (j * gap, 0), (j * gap, WIDTH))

def draw_screen(grid):
    WIN.fill(GREY)
    for row in grid:
        for spot in row:
            spot.draw_spot()
    # draw_grid()
    pygame.display.update()

def get_mouse_pos(pos):
    x, y = pos
    gap = WIDTH // ROWS
    row = x // gap
    col = y // gap
    return row, col

def check_for_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def main():
    # pygame.init()
    # FONT = pygame.font.Font('freesansbold.ttf', 20)

    grid = make_grid()

    start = None
    end = None

    running = True

    while running:

        draw_screen(grid)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != start and spot != end:
                    spot.make_wall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                spot = grid[row][col]
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
                spot.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    path_found = astar_pathfinder(lambda: draw_screen(grid), grid, start, end)

                    if not path_found:
                        # not_found = FONT.render('Sorry! This maze cannot be solved. Press "C" to continue...', 1, RED)
                        # rect = not_found.get_rect()
                        # rect.topleft = (WIDTH // 2) - (not_found.get_width() // 2), 10
                        # WIN.blit(not_found, rect)
                        pygame.display.set_caption("Sorry! This maze cannot be solved. Press C to continue...")
                        waiting = True
                        while waiting:
                            check_for_quit()

                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_c:
                                        start = None
                                        end = None
                                        grid = make_grid()
                                        waiting = False
                        pygame.display.set_caption("Maze Solver")

                    if path_found:
                        # found = FONT.render('Shortest Path Found!. Press "C" to continue...', 1, GREEN)
                        # rect = found.get_rect()
                        # rect.topleft = (WIDTH // 2) - (found.get_width() // 2), 10
                        # WIN.blit(found, rect)
                        pygame.display.set_caption("Shortest Path Found! Press C to continue...")
                        waiting = True
                        while waiting:
                            check_for_quit()

                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_c:
                                        start = None
                                        end = None
                                        grid = make_grid()
                                        waiting = False
                        pygame.display.set_caption("Maze Solver")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

    pygame.quit()


main()




