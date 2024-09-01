import pygame
from pygame.locals import *
import time

GRSZ = 20  # Grid Size
BLACK = (78, 78, 78)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)

running = True
pygame.init()
cells_width = 1200 // GRSZ - 5
cells_height = 800 // GRSZ - 5
window = pygame.display.set_mode((cells_width * GRSZ, cells_height * GRSZ))


class Cell():
    def __init__(self, alive=False, x=0, y=0):
        self.alive = alive
        self.cx = x * GRSZ
        self.cy = y * GRSZ

    def __str__(self):
        if self.alive:
            return 'O'
        else:
            return 'X'

    def undead(self):
        clk_x, clk_y = pygame.mouse.get_pos()
        i, j = clk_x // GRSZ, clk_y // GRSZ
        field[j][i].alive = True
    def dead(self):
        clk_x, clk_y = pygame.mouse.get_pos()
        i, j = clk_x // GRSZ, clk_y // GRSZ
        field[j][i].alive = False


class Cube:
    def update(self):
        self.cx, self.cy = pygame.mouse.get_pos()
        self.square = pygame.Rect((self.cx // GRSZ) * GRSZ, (self.cy // GRSZ) * GRSZ, GRSZ, GRSZ)

    def draw(self):
        pygame.draw.rect(window, 'white', self.square)


field = [[Cell(False, i, j) for i in range(cells_width)] for j in range(cells_height)]

cube = Cube()
drawing_cube = False

cell = Cell()

while running:
    window.fill(GREY)

    # for i in range(0, window.get_height() // GRSZ):
    #     pygame.draw.line(window, BLACK, (0, i * GRSZ), (window.get_width(), i * GRSZ))
    #
    # for j in range(0, window.get_width() // GRSZ):
    #     pygame.draw.line(window, BLACK, (j * GRSZ, 0), (j * GRSZ, window.get_height()))

    for row in field:
        for cell in row:
            if not cell.alive:
                square = Rect(cell.cx, cell.cy, GRSZ, GRSZ)
                pygame.draw.rect(window, BLACK, square, 1)
            else:
                square = Rect(cell.cx, cell.cy, GRSZ, GRSZ)
                pygame.draw.rect(window, WHITE, square)

    # if drawing_cube:
    #     cube.draw()
    # pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # cube.update()
                # drawing_cube = True
                cell.undead()
            elif event.button == 3:
                cell.dead()
    pygame.display.flip()

    pygame.display.update()
