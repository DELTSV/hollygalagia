from math import sin, cos, radians, degrees, sqrt, asin
from time import time
import arcade

from source.constant import *
from source.effect.EnemyExplosion import EnemyExplosion


class Enemy(arcade.Sprite):
    def __init__(self, x: int, y: int, texture_list, enter: int, alt: bool):
        self.__state = 0
        self.orientation = 0
        super().__init__(
            scale=SPRITE_SCALING,
            hit_box_algorithm='Simple'
        )
        self.textures = texture_list
        if enter == 1:
            self.__positions = self.enter_1(alt)
        self.__idle = (x, y)

    def take_damage(self):
        return self.explode()

    def explode(self):
        return EnemyExplosion(int(self.center_x), int(self.center_y))

    def next_in_circle(self, center: (int, int), start_angle: float, radius: int, reverse=False):
        if reverse:
            angle = (start_angle + 180 - degrees(ENEMY_SPEED / radius)) % 360
        else:
            angle = (start_angle + degrees(ENEMY_SPEED / radius)) % 360
        return (
            sin(radians(angle)) * radius + center[0],
            cos(radians(angle)) * radius + center[1],
            (angle + 90 - (180 if reverse else 0)) % 360)

    def enter_1(self, left=False):
        angle = 180
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT
        yield x, y, angle
        while angle > 100 if not left else angle < 260:
            tmp = self.next_in_circle(
                (WINDOW_WIDTH / 2 + (-300 if left else 300), WINDOW_HEIGHT),
                angle - 90,
                300,
                not left
            )
            x, y, angle = tmp
            yield tmp
        if left:
            circle_y = y + cos(radians((angle - 90))) * 100
            circle_x = x + sin(radians((angle - 90))) * 100
        else:
            circle_y = y - cos(radians((angle - 90))) * 100
            circle_x = x - sin(radians((angle - 90))) * 100
        while angle < 315:
            tmp = self.next_in_circle((circle_x, circle_y), angle - 90, 100, left)
            x, y, angle = tmp
            yield tmp
        while (x, y) != self.__idle:
            to_do = sqrt((abs(self.__idle[0] - x) ** 2) + (abs(self.__idle[1] - y) ** 2))
            angle = ((degrees(asin(abs(y - self.__idle[1]) / to_do)) - 90) % 360 + 360) % 360
            if to_do < ENEMY_SPEED:
                x, y = self.__idle
            else:
                if x < self.__idle[0]:
                    x += ENEMY_SPEED / to_do * abs(self.__idle[0] - x)
                else:
                    x -= ENEMY_SPEED / to_do * abs(self.__idle[0] - x)
                if y < self.__idle[1]:
                    y += ENEMY_SPEED / to_do * abs(self.__idle[1] - y)
                else:
                    y -= ENEMY_SPEED / to_do * abs(self.__idle[1] - y)
            yield x, y, angle
        yield x, y, 0

    def update(self):
        try:
            new_pos = next(self.__positions)
            self.center_x = new_pos[0]
            self.center_y = new_pos[1]
            self.orientation = new_pos[2]
        except StopIteration:
            pass
        if int(time() % 2) == 0 and self.__state == 0:
            self.__state = 1
        elif int(time() % 2) == 1:
            self.__state = 0
        self.set_texture(self.get_texture_index())

    def get_texture_index(self):
        angle = abs(self.orientation % 90)
        if angle < 7.5:
            if self.__state == 0:
                index = 6
            else:
                index = 7
        elif angle < 22.5:
            index = 5
        elif angle < 37.5:
            index = 4
        elif angle < 52.5:
            index = 3
        elif angle < 67.5:
            index = 2
        elif angle < 82.5:
            index = 1
        else:
            index = 0
        if self.orientation < 90:
            return index
        elif self.orientation < 180:
            return 7 - index + 8
        elif self.orientation < 270:
            return index + 16
        else:
            return 7 - index + 24
