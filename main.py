import time
import datetime
import random
from patterns import *
from functions import *

# Game settings
GRSZ = 20  # Grid Size
cells_width = 20
cells_height = 20
time_delay = 0.1
# Colors
BLACK = (78, 78, 78)  # Grid
GREY = (100, 100, 100)  # Background
GREEN = (0, 100, 0)  # Background
# Control Keys
START_GAME = pygame.K_F1
CLEAR_FIELD = pygame.K_SPACE
RANDOM_FILL = pygame.K_r
SPEED_UP = pygame.K_RIGHT
SLOW_DOWN = pygame.K_LEFT
FILL = pygame.K_f
PATTERN_MODE = pygame.K_p

running = True
game_started = False
pattern_mode = False
pygame.init()
window = pygame.display.set_mode((cells_width * GRSZ, cells_height * GRSZ))

field = [[False for i in range(cells_width)] for j in range(cells_height)]
new_field = [[False for i in range(cells_width)] for j in range(cells_height)]
step_sum_time = []
pattern = glider

while running:
    window.fill(GREY)
    start_render = datetime.datetime.now()

    if pattern_mode and pattern:
        draw_pattern(window, pattern, GRSZ, GREEN)
        draw_cells(window, field, cells_width, cells_height, GRSZ, 'white', BLACK)
    else:
        draw_cells(window, field, cells_width, cells_height, GRSZ, 'white', BLACK)

    end_render = datetime.datetime.now()
    start = datetime.datetime.now()

    if game_started:

        count_neighbours = {}
        for j in range(cells_height):
            for i in range(cells_width):
                count_neighbours[(i, j)] = check_neighbours(i, j, field, cells_width, cells_height)

        temp_field = field.copy()
        for (i, j), n in count_neighbours.items():
            if not temp_field[j][i]:
                if n == 3:
                    undead(i, j, field)
            else:
                if n not in (2, 3):
                    dead(i, j, field)

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
                undead(i, j, field)
                if pattern_mode:
                    create_pattern(clk_x, clk_y, pattern, GRSZ, field)
            elif event.button == 3:
                clk_x, clk_y = pygame.mouse.get_pos()
                i, j = clk_x // GRSZ, clk_y // GRSZ
                dead(i, j, field)
        # Keyboard controls
        elif event.type == pygame.KEYDOWN:
            # Clear Field
            if event.key == CLEAR_FIELD:
                for i in range(cells_width):
                    for j in range(cells_height):
                        dead(i, j, field)
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
                            dead(i, j, field)
                        else:
                            undead(i, j, field)
            # Pattern Mode
            elif event.key == PATTERN_MODE:
                if pattern_mode:
                    pattern_mode = False
                else:
                    pattern_mode = True
    pygame.display.flip()

    pygame.display.update()
