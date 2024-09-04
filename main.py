import time
import datetime
import random
import pygame
import pygame_gui
from patterns import *
from functions import *
from tkinter import *
from tkinter import messagebox

pygame.init()
# Game settings
GRSZ = 20  # Grid Size
cells_width = 70
cells_height = 35
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

window = pygame.display.set_mode((cells_width * GRSZ, cells_height * GRSZ))
background = pygame.Surface((cells_width * GRSZ, cells_height * GRSZ))
background.fill(pygame.Color(GREY))

manager = pygame_gui.UIManager((cells_width * GRSZ, cells_height * GRSZ), theme_path='theme.json')

clock = pygame.time.Clock()

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRSZ, GRSZ), (80, 40)), text='Start',
                                            manager=manager)

patterns_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRSZ, GRSZ * 2 + 40), (80, 40)),
                                               text='Patterns', manager=manager)

clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRSZ, GRSZ * 3 + 80), (80, 40)),
                                            text='Clear', manager=manager)

random_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRSZ, GRSZ * 4 + 120), (80, 40)),
                                             text='Random', manager=manager)

help_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((GRSZ, GRSZ * 5 + 160), (80, 40)),
                                           text='Help', manager=manager)

field = [[False for i in range(cells_width)] for j in range(cells_height)]
new_field = [[False for i in range(cells_width)] for j in range(cells_height)]
step_sum_time = []
pattern = glider

while running:
    window.blit(background, (0, 0))
    time_delta = clock.tick(60) / 1000.0
    start_render = datetime.datetime.now()

    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                if game_started:
                    game_started = False
                    start_button.set_text('Stop')
                else:
                    game_started = True
                    start_button.set_text('Start')
            elif event.ui_element == clear_button:
                for i in range(cells_width):
                    for j in range(cells_height):
                        dead(i, j, field)
            elif event.ui_element == patterns_button:
                if pattern_mode:
                    pattern_mode = False
                else:
                    pattern_mode = True
            elif event.ui_element == random_button:
                for i in range(cells_width):
                    for j in range(cells_height):
                        r = random.randint(0, 1)
                        if r == 0:
                            dead(i, j, field)
                        else:
                            undead(i, j, field)
            elif event.ui_element == help_button:
                messagebox.showinfo('Help','OK')
        # Cell editing with mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            clk_x, clk_y = pygame.mouse.get_pos()
            if (not start_button.hover_point(clk_x, clk_y)
                    and not patterns_button.hover_point(clk_x, clk_y)
                    and not clear_button.hover_point(clk_x, clk_y)
                    and not random_button.hover_point(clk_x, clk_y)
                    and not help_button.hover_point(clk_x, clk_y)):
                if event.button == 1:
                    i, j = clk_x // GRSZ, clk_y // GRSZ
                    undead(i, j, field)
                    print(start_button.hover_point(clk_x, clk_y))
                    if pattern_mode:
                        create_pattern(clk_x, clk_y, pattern, GRSZ, field)
                elif event.button == 3:
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
            elif event.key == K_1:
                pattern = glider
            elif event.key == K_2:
                pattern = lspaceship
            elif event.key == K_3:
                pattern = galaxy_oscillator
            elif event.key == K_4:
                pattern = tetris_idk_lol

    manager.update(time_delta)
    manager.draw_ui(window)

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
    manager.draw_ui(window)
    pygame.display.flip()

    pygame.display.update()
