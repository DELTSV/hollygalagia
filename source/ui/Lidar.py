import arcade

from source.constant import PLAYER_LINE, WINDOW_HEIGHT, CHAR_SPRITE_SIZE, MISSILE_SPRITE_SIZE
from source.ui.Radar import EMPTY, ENEMY, MISSILE, ENEMY_AND_MISSILE


class Lidar:
    def __init__(self, x, enemies):
        self.__x = x
        arcade.draw_line(x, PLAYER_LINE, x, WINDOW_HEIGHT, arcade.color.RED)
        self.__enemies = enemies

    def detect_nearest_object(self):
        nearest = WINDOW_HEIGHT
        obj = EMPTY
        for e in self.__enemies:
            if e.center_x - CHAR_SPRITE_SIZE / 2 <= self.__x <= e.center_x + CHAR_SPRITE_SIZE / 2:
                if e.center_y < nearest:
                    obj = ENEMY
                elif e.center_y == nearest and obj == MISSILE:
                    obj = ENEMY_AND_MISSILE
                nearest = e.center_y
            for m in e.missiles:
                if m.center_x - MISSILE_SPRITE_SIZE / 2 <= self.__x <= m.center_x + MISSILE_SPRITE_SIZE / 2:
                    if m.center_y < nearest:
                        obj = MISSILE
                    elif m.center_y == nearest and obj == ENEMY:
                        obj = ENEMY_AND_MISSILE
                    nearest = e.center_y
        return obj

    def draw(self):
        arcade.draw_line(self.__x, PLAYER_LINE, self.__x, WINDOW_HEIGHT, arcade.color.RED)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x
