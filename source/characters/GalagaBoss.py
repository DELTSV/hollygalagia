import arcade

from source.characters.Enemy import Enemy
from source.constant import *


class GalagaBoss(Enemy):
    def __init__(self, x: int, y: int):
        self.__hp = 2
        coords1 = [(float((i * (CHAR_SPRITE_SIZE + 2)) + ENEMY1_STATE1_SPRITE_ORIGIN[0]),
                    float(ENEMY1_STATE1_SPRITE_ORIGIN[1]), float(CHAR_SPRITE_SIZE),
                    float(CHAR_SPRITE_SIZE))
                   for i in range(0, 8)]
        coords2 = [(float((i * (CHAR_SPRITE_SIZE + 2)) + ENEMY1_STATE2_SPRITE_ORIGIN[0]),
                    float(ENEMY1_STATE2_SPRITE_ORIGIN[1]), float(CHAR_SPRITE_SIZE),
                    float(CHAR_SPRITE_SIZE))
                   for i in range(0, 8)]
        textures = arcade.load_textures(
            SPRITE_FILE,
            coords1 + coords2,
            mirrored=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1 + coords2,
            flipped=True,
            mirrored=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1 + coords2,
            flipped=True,
            hit_box_algorithm='Simple'
        )
        textures += arcade.load_textures(
            SPRITE_FILE,
            coords1 + coords2,
            hit_box_algorithm='Simple'
        )
        super().__init__(x, y, textures)

    def take_damage(self):
        self.__hp -= 1
        if self.__hp == 0:
            return self.explode()

    def get_texture_index(self):
        index = super().get_texture_index()
        quart = int(self.orientation / 90)
        if self.__hp == 2:
            return index + quart * 8
        else:
            return index + (quart + 1) * 8
