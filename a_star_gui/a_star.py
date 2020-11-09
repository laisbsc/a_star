import pygame
import math
from queue import PriorityQueue

# setup the square display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption(("The A* Path-finding algortithm"))

# declare the colour codes
WHITE = (255, 255, 255)  # blank grid, node not yet visited
BLACK = (0, 0, 0)  # barrier, node cannot be visited
RED = (255, 0, 0)  # node which has been visited
GREEN = (0, 255, 0)  # nodes in the open set [?]
ORANGE = (255, 165, 0)  # start node
PURPLE = (128, 0, 128)  # path from start-node to goal-node
TURQUOISE = (64, 224, 208)  # goal-node
GREY = (128, 128, 128)  # colour of the lines in the grid


class Node:
    '''
    Nodes in the grid which will hold:
    - location (x, y positions) of itself in the grid;
    - the dimensions of itself;
    - the location of its neighbours.
    '''

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width  # since it is a squared grid
        self.width = width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_position(self):
        '''
        Fetches the position of the node in the grid
        :return: (row, col) coordinates
        '''
        return self.row, self.col

    def is_closed(self):
        '''
        Changes the colours of the visited nodes to RED
        '''
        return self.row == RED

    def is_open(self):
        return self.color == GREEN

    def barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        '''
        Draw the nodes on the grid
        :param win: window grid from pygame
        :return:
        '''
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        '''
        Keeps track of all neighbours (non-barries) in the neighbours' list
        :param grid:
        :return:
        '''
        self.neighbors = []
        # check if the current row is less than total rows minus 1
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier(): #moving down rows
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].barrier(): #moving up rows
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier(): #moving right columns
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and not grid[self.row][self.col - 1].barrier(): #moving left rows
            self.neighbors.append(grid[self.row - 1][self.col - 1])

    def __lt__(self, other):
        '''
        handles the comparison of two nodes against each other
        :param other:
        :return:
        '''
        return False


def heur(p1, p2):
    '''
    Define th heuristics distance function needed for the algorithm. In this case, Manhattan distance is used.
    :param p1: vector distance of point 1 on the grid (x1, y1)
    :param p2: vector distance of point 2 on the grid (x2, y2)
    :return: absolute distance between points nodes
    '''
    x1, y1 = p1
    x2, y2 = p2
    m_distance = abs(x1 - x2) * abs(y1 - y2)
    return m_distance


def search_alg(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heur(start.get_pos(), end.get_pos())

    open_set_hash = {start} # will check what is in the PriorityQueue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            #make path
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + heur(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

        return False

def make_grid(rows, width):
    # list that can hold all nodes and its positions
    grid = []
    gap = width // rows  # returns the gap between each row
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


# draw the nodes
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)  # fills the frame with https://youtu.be/JtiK0DOeI4A?t=2629

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()  # take what was just drawn and update the display


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    '''
    Determine all the checks such as collision, type of node, etc.
    :param win:
    :param width:
    :return:
    '''
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # when left mouse-button is clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # when right mouse-button is clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start == None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                        # search_alg(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        if event.key == pygame.K_c:
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
