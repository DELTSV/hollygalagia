import random

import arcade

from source.constant import WINDOW_HEIGHT, WINDOW_WIDTH


class Star:
    def __init__(self):
        self.__x = random.randrange(0, WINDOW_WIDTH)
        self.__y = random.randrange(0, WINDOW_HEIGHT + 50)
        self.__speed = random.randrange(2, 5)
        self.__alpha = 255

    def reset_pos(self):
        self.__y = random.randrange(0, WINDOW_HEIGHT)
        self.__x = random.randrange(0, WINDOW_WIDTH)
        self.__alpha = 255

    def on_draw(self):
        arcade.draw_circle_filled(self.__x, self.__y, 2, (255, 255, 255, self.__alpha), num_segments=2)

    def on_update(self):
        self.__y -= self.__speed
        self.__alpha -= self.__speed
        if self.__y < 0 or self.__alpha < 0:
            self.reset_pos()
