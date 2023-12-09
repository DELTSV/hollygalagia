import arcade

from source.constant import *
from source.effect.Explosion import Explosion


class PlayerExplosion(Explosion):
    def __init__(self, x: int, y: int):
        coords = [(float((i * (EXPLOSION_SPRITE_SIZE + 2)) + EXPLOSION_PLAYER_SPRITE_ORIGIN[0]), float(EXPLOSION_PLAYER_SPRITE_ORIGIN[1]), float(EXPLOSION_SPRITE_SIZE), float(EXPLOSION_SPRITE_SIZE)) for i in range(0, 4)]
        texture_list = arcade.load_textures(
            SPRITE_FILE,
            coords,
            hit_box_algorithm=None
        )
        super().__init__(texture_list, x, y)
