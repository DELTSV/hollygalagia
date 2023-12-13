from source.characters.Enemy import Enemy
from source.constant import *
import arcade

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
