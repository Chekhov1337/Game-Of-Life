import patterns
import pygame
from pygame.locals import *


def undead(i, j, field):
    field[j][i] = True


def dead(i, j, field):
    field[j][i] = False


def check_neighbours(i, j, field, cells_width, cells_height):
    n = 0
    neighbours = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]

    for k, m in neighbours:
        if 0 <= i + k <= cells_width - 1 and 0 <= j + m <= cells_height - 1:
            if field[j + m][i + k]:
                n += 1
    return n

def draw_cells(surface, cells_width, cells_height, gridsize = 20, alive_color = (0,0,0), dead_color = (78,78,78)):
    for j in range(cells_height):
        for i in range(cells_width):
            if field[j][i]:
                square = Rect(i * gridsize, j * gridsize, gridsize, gridsize)
                pygame.draw.rect(surface, alive_color, square)
            else:
                square = Rect(i * gridsize, j * gridsize, gridsize, gridsize)
                pygame.draw.rect(surface, dead_color, square, 1)

def draw_pattern(surface, pattern=patterns.glider, gridsize=20, color=(0, 100, 0)):
    sx, sy = pygame.mouse.get_pos()
    si, sj = sx // gridsize, sy // gridsize
    for pi, pj in pattern:
        square = Rect((si + pi) * gridsize, (sj + pj) * gridsize, gridsize, gridsize)
        pygame.draw.rect(surface, color, square)

def create_pattern(clk_x, clk_y, pattern, gridsize, field):
    si, sj = clk_x // gridsize, clk_y // gridsize
    for pi, pj in pattern:
        undead(si + pi, sj + pj, field)