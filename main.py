import datetime

import pygame
from pygame.locals import *
import time
import datetime
import random
import statistics

# Game settings
GRSZ = 10  # Grid Size
cells_width = 160
cells_height = 80
time_delay = 0.1
# Colors for grid
BLACK = (78, 78, 78)  # Grid
GREY = (100, 100, 100)  # Background
# Control Keys
START_GAME = pygame.K_F1
CLEAR_FIELD = pygame.K_SPACE
RANDOM_FILL = pygame.K_r
SPEED_UP = pygame.K_RIGHT
SLOW_DOWN = pygame.K_LEFT
FILL = pygame.K_f

running = True
game_started = False
pygame.init()
window = pygame.display.set_mode((cells_width * GRSZ, cells_height * GRSZ))


def undead(i, j):
    field[j][i] = True


def dead(i, j):
    field[j][i] = False


def check_neighbours(i, j):
    n = 0
    neighbours = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]

    for k, m in neighbours:
        if 0 <= i + k <= cells_width - 1 and 0 <= j + m <= cells_height - 1:
            if field[j + m][i + k]:
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


field = [[False for i in range(cells_width)] for j in range(cells_height)]
new_field = [[False for i in range(cells_width)] for j in range(cells_height)]
step_sum_time = []

while running:
    window.fill(GREY)
    start_render = datetime.datetime.now()

    for j in range(cells_height):
        for i in range(cells_width):
            if field[j][i]:
                square = Rect(i * GRSZ, j * GRSZ, GRSZ, GRSZ)
                pygame.draw.rect(window, 'white', square)
            else:
                square = Rect(i * GRSZ, j * GRSZ, GRSZ, GRSZ)
                pygame.draw.rect(window, BLACK, square, 1)

    end_render = datetime.datetime.now()
    start = datetime.datetime.now()

    if game_started:

        count_neighbours = {}
        for j in range(cells_height):
            for i in range(cells_width):
                count_neighbours[(i, j)] = check_neighbours(i, j)

        temp_field = field.copy()
        for (i, j), n in count_neighbours.items():
            if not temp_field[j][i]:
                if n == 3:
                    undead(i, j)
            else:
                if n not in (2, 3):
                    dead(i, j)

    end = datetime.datetime.now()
    delta = (end - start_render).total_seconds()
    if time_delay > delta:
        time.sleep(time_delay - delta)

    # if game_started:
    #     step_sum_time.append(delta.total_seconds())
    # if len(step_sum_time) == 100:
    #     print(f'Average time: {statistics.mean(step_sum_time)}')
    #     running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Cell editing with mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clk_x, clk_y = pygame.mouse.get_pos()
                i, j = clk_x // GRSZ, clk_y // GRSZ
                undead(i, j)
            elif event.button == 3:
                clk_x, clk_y = pygame.mouse.get_pos()
                i, j = clk_x // GRSZ, clk_y // GRSZ
                dead(i, j)
        # Keyboard controls
        elif event.type == pygame.KEYDOWN:
            # Clear Field
            if event.key == CLEAR_FIELD:
                for i in range(cells_width):
                    for j in range(cells_height):
                        dead(i, j)
            # Start/Stop Game
            elif event.key == START_GAME:
                if game_started:
                    game_started = False
                else:
                    game_started = True
                print('Game started' if game_started else 'Game stopped')
            # Steps speed control
            elif event.key == SPEED_UP:
                if time_delay != 0:
                    time_delay -= 0.1
            elif event.key == SLOW_DOWN:
                time_delay += 0.1
            # Random Fill
            elif event.key == RANDOM_FILL:
                for i in range(cells_width):
                    for j in range(cells_height):
                        r = random.randint(0, 1)
                        if r == 0:
                            dead(i, j)
                        else:
                            undead(i, j)
    pygame.display.flip()

    pygame.display.update()
