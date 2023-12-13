from math import sin, cos, radians, degrees, sqrt, asin
from time import time
from random import randint
import arcade

from source.characters.Player import Player
from source.constant import *
from source.effect.EnemyExplosion import EnemyExplosion
from source.effect.PlayerExplosion import PlayerExplosion
from source.weapons.EnemyMissile import EnemyMissile
from utils import mod


class Enemy(arcade.Sprite):
    def __init__(self, x: int, y: int, texture_list, difficulty: int, enter: int, alt: bool):
        self.__state = 0
        self.orientation = 0
        super().__init__(
            scale=SPRITE_SCALING,
            hit_box_algorithm='Simple'
        )
        self.textures = texture_list
        if enter == 1:
            self.__positions = self.enter_1(alt)
        elif enter == 2:
            self.__positions = self.enter_2(alt)
        self.__idle = (x, y)
        self.is_idle = False
        self.__difficulty = difficulty
        self.__missiles = arcade.SpriteList()

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
        start_x = WINDOW_WIDTH / 2 + (15 if left else -15) * SPRITE_SCALING
        x = start_x
        y = WINDOW_HEIGHT
        radius = 80 * SPRITE_SCALING
        yield x, y, angle
        while angle > 90 if not left else angle < 260:
            x, y, angle = self.next_in_circle(
                (start_x + (-radius if left else radius), WINDOW_HEIGHT),
                angle - 90,
                radius,
                not left
            )
            yield x, y, angle
        radius = 35 * SPRITE_SCALING
        if left:
            circle_y = y + cos(radians((angle - 90))) * radius
            circle_x = x + sin(radians((angle - 90))) * radius
        else:
            circle_y = y - cos(radians((angle - 90))) * radius
            circle_x = x - sin(radians((angle - 90))) * radius
        while angle < 315:
            x, y, angle = self.next_in_circle((circle_x, circle_y), angle - 90, radius, left)
            if 290 < angle < 300 or 110 < angle < 120:
                if randint(0, 100) < 5 * self.__difficulty:
                    self.shoot(x, y)
            yield x, y, angle
        for move in self.end_move(x, y):
            yield move

    def shoot(self, x, y):
        self.__missiles.append(EnemyMissile(x, y))


    def enter_2(self, left=False):
        angle = 90 if left else 270
        start_x = 0 if left else WINDOW_WIDTH
        start_y = PLAYER_LINE + 2 * CHAR_SPRITE_SIZE * SPRITE_SCALING
        x = start_x
        y = start_y
        radius = 60 * SPRITE_SCALING
        yield x, y, angle
        while int(angle) > 5 if left else int(angle) < 350:
            x, y, angle = self.next_in_circle((start_x, start_y + radius), angle - 90, radius, left)
            yield x, y, angle
        start_y = y
        radius = 25 * SPRITE_SCALING
        start_x = x - (-sin(radians(angle - 90)) if left else sin(radians(angle - 90))) * radius
        start_angle = int(angle) + (-1 if left else 1)
        circle = 0
        while True:
            x, y, new_angle = self.next_in_circle((start_x, start_y), angle - 90, radius, left)
            if left and new_angle - start_angle <= 0 < angle - start_angle:
                if circle == 0:
                    circle = 1
                else:
                    break
            if not left and new_angle - start_angle >= 0 > angle - start_angle:
                if circle == 0:
                    circle = 1
                else:
                    break
            angle = new_angle
            yield x, y, angle
        if randint(0, 100) < 5 * self.__difficulty:
            print("shoot")
            self.shoot(x, y)
        for move in self.end_move(x, y):
            yield move


    def end_move(self, x, y):
        while (x, y) != self.__idle:
            to_do = sqrt((abs(self.__idle[0] - x) ** 2) + (abs(self.__idle[1] - y) ** 2))
            angle = mod(int((degrees(asin(abs(y - self.__idle[1]) / to_do)) - 90)), 360)
            if self.__idle[0] > x:
                angle = (90 - angle) + 90
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
        self.is_idle = True

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
        self.__missiles.update()

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw(filter=filter, pixelated=pixelated, blend_function=blend_function)
        self.__missiles.draw(filter=filter, pixelated=pixelated, blend_function=blend_function)

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

    def detect_missile_hit_player(self, player: Player) -> PlayerExplosion | None:
        hit_list = arcade.check_for_collision_with_list(player.sprite, self.__missiles)
        for m in hit_list:
            m.remove_from_sprite_lists()
        if len(hit_list) > 0:
            return player.explode()
        return None
