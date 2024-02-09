import random
from math import sin, cos, radians, acos, asin

from source.characters.Enemy import Enemy
from source.constant import *
import arcade

from utils import mod


class Goei(Enemy):
    def __init__(self, x: int, y: int, difficulty: int, enter: int, alt: bool):
        coords1 = [(float((i * (CHAR_SPRITE_SIZE + 2)) + ENEMY2_SPRITE_ORIGIN[0]),
                    float(ENEMY2_SPRITE_ORIGIN[1]), float(CHAR_SPRITE_SIZE),
                    float(CHAR_SPRITE_SIZE))
                   for i in range(0, 8)]
        textures = arcade.load_textures(
            SPRITE_FILE,
            coords1,
            mirrored=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1,
            flipped=True,
            mirrored=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1,
            flipped=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1,
            hit_box_algorithm='Simple'
        )
        super().__init__(x, y, textures, difficulty, enter, alt)

    def end_attack(self, x, y):
        yield x, y, 180
        up = False
        while True:
            if 175 < self.orientation < 185 and random.randint(0, 100) < 15:
                self.shoot(self.center_x, self.center_y)
            action = random.randint(0, 2)
            if up and self.center_y < self.idle[1]:
                for move in self.end_move():
                    yield move
                break
            if action == 0:
                for nx, ny, angle in self.turn():
                    if ny < - (CHAR_SPRITE_SIZE * SPRITE_SCALING) / 2:
                        ny = CHAR_SPRITE_SIZE * SPRITE_SCALING + WINDOW_HEIGHT
                        yield nx, ny, angle
                        up = True
                    else:
                        yield nx, ny, angle
            elif action == 1:
                for nx, ny in self.line():
                    yield nx, ny, self.orientation

    def turn(self):
        radius = random.randint(20, 35) * SPRITE_SCALING
        angle = self.orientation
        revert = True if angle > 180 else (False if angle < 180 else random.randint(0, 2) == 1)
        if revert:
            center_x = self.center_x + sin(radians(mod(int(angle) - 90, 360))) * radius
            center_y = self.center_y + cos(radians(mod(int(angle) - 90, 360))) * radius
        else:
            center_x = self.center_x - sin(radians(mod(int(angle) - 90, 360))) * radius
            center_y = self.center_y - cos(radians(mod(int(angle) - 90, 360))) * radius
        for i in range(0, random.randint(30, 100)):
            x, y, angle = self.next_in_circle((center_x, center_y), mod(angle - 90, 360), radius, revert)
            yield x, y, angle
            if not 45 < angle < 315:
                break

    def line(self):
        h = PLAYER_SPEED
        for i in range(0, random.randint(10, 30)):
            alpha = radians(mod(self.orientation + 90, 360))
            o = abs(sin(alpha) * h)
            a = abs(cos(alpha) * h)
            if 0 <= self.orientation <= 90:
                yield self.center_x + a, self.center_y + o
            elif 90 < self.orientation <= 180:
                yield self.center_x + a, self.center_y - o
            elif 180 < self.orientation <= 270:
                yield self.center_x - a, self.center_y - o
            else:
                yield self.center_x - a, self.center_y + o
            if self.center_x < 0 and self.orientation > 180:
                break
            if self.center_x > WINDOW_WIDTH and self.orientation < 180:
                break
