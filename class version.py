import datetime

import pygame
from pygame.locals import *
import time
import datetime
import random
import statistics

# Game settings
GRSZ = 1  # Grid Size
cells_width = 1280
cells_height = 720
time_delay = 0.1
# Colors for grid
BLACK = (78, 78, 78)  # Grid
GREY = (100, 100, 100)  # Background

running = True
game_started = False
pygame.init()
window = pygame.display.set_mode((cells_width * GRSZ, cells_height * GRSZ))


def undead(i, j):
    cell_l = field[j][i]
    cell_l.alive = True


def dead(i, j):
    cell_l = field[j][i]
    cell_l.alive = False


def check_neighbours(cell):
    i = cell.i
    j = cell.j
    n = 0
    neighbours = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]

    for k, m in neighbours:
        if 0 <= i + k <= cells_width - 1 and 0 <= j + m <= cells_height - 1:
            if field[j + m][i + k].alive is True:
                n += 1

    return n


class Cell():
    def __init__(self, alive=False, i=0, j=0):
        self.alive = alive
        self.i = i
        self.j = j

        self.cx = i * GRSZ
        self.cy = j * GRSZ

    def __str__(self):
        if self.alive:
            return 'O'
        else:
            return 'X'


field = [[Cell(False, i, j) for i in range(cells_width)] for j in range(cells_height)]
new_field = [[Cell(False, i, j) for i in range(cells_width)] for j in range(cells_height)]

step_sum_time = []

while running:
    window.fill(GREY)
    start_render = datetime.datetime.now()

    for row in field:
        for cell in row:
            if cell.alive:
                square = Rect(cell.cx, cell.cy, GRSZ, GRSZ)
                pygame.draw.rect(window, 'white', square)
            else:
                square = Rect(cell.cx, cell.cy, GRSZ, GRSZ)
                pygame.draw.rect(window, BLACK, square, 1)

    end_render = datetime.datetime.now()
    print(f'Render time: {end_render - start_render}')

    start = datetime.datetime.now()
    if game_started:

        count_neighbours = {}
        for row in field:
            for cell in row:
                count_neighbours[cell] = check_neighbours(cell)

        temp_field = field.copy()
        for cell, n in count_neighbours.items():
            if not temp_field[cell.j][cell.i].alive:
                if n == 3:
                    undead(cell.i, cell.j)
            else:
                if n not in (2, 3):
                    dead(cell.i, cell.j)
        time.sleep(time_delay)


    end = datetime.datetime.now()
    print(f'One step time: {end - start}')
    delta = end - start_render
    if game_started:
        step_sum_time.append(delta.total_seconds())
    if len(step_sum_time) == 100:
        print(f'AVerage time: {statistics.mean(step_sum_time)}')
        running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clk_x, clk_y = pygame.mouse.get_pos()
                i, j = clk_x // GRSZ, clk_y // GRSZ
                undead(i, j)
            elif event.button == 3:
                clk_x, clk_y = pygame.mouse.get_pos()
                i, j = clk_x // GRSZ, clk_y // GRSZ
                dead(i, j)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(cells_width):
                    for j in range(cells_height):
                        dead(i, j)
            elif event.key == pygame.K_F1:
                if game_started:
                    game_started = False
                else:
                    game_started = True
                print('Game started' if game_started else 'Game stopped')
            elif event.key == pygame.K_RIGHT:
                if time_delay != 0:
                    time_delay -= 0.1
            elif event.key == pygame.K_LEFT:
                time_delay += 0.1
            elif event.key == pygame.K_r:
                for i in range(cells_width):
                    for j in range(cells_height):
                        r = random.randint(0, 1)
                        if r == 0:
                            dead(i, j)
                        else:
                            undead(i, j)

    pygame.display.flip()

    pygame.display.update()
