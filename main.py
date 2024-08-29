import pygame as pg
from pygame.locals import *

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)

window = pg.display.set_mode((1000, 500))

while True:
    window.fill(GREY)

    for i in range(0, window.get_height() // 20):
        pg.draw.line(window, BLACK, (0, i * 20), (window.get_width(), i * 20))

    for j in range(0, window.get_width() // 20):
        pg.draw.line(window, BLACK, (j * 20, 0), (j * 20, window.get_height()))

    for i in pg.event.get():
        if i.type == QUIT:
            quit()

    pg.display.update()

