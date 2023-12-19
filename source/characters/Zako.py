import random
from math import sqrt, degrees, asin

from source.characters.Enemy import Enemy
from source.constant import *
import arcade

from utils import mod


class Zako(Enemy):
    def __init__(self, x: int, y: int, difficulty: int, enter: int, alt: bool):
        coords1 = [(float((i * (CHAR_SPRITE_SIZE + 2)) + ENEMY3_SPRITE_ORIGIN[0]),
                    float(ENEMY3_SPRITE_ORIGIN[1]), float(CHAR_SPRITE_SIZE),
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
        dest_x = random.randint(0, WINDOW_WIDTH)
        dest_y = PLAYER_LINE
        for m in self.goto(dest_x, dest_y):
            x, y, angle = m
            yield m
        left = random.randint(0, 1) == 1
        angle = 180
        radius = 10 * SPRITE_SCALING
        yield x, y, angle
        start_x = x + (radius if left else - radius)
        start_y = y
        while 0 <= angle <= 180 if left else angle >= 180:
            x, y, angle = self.next_in_circle((start_x, start_y), angle - 90, radius, left)
            yield x, y, angle
        for m in self.end_move():
            yield m
