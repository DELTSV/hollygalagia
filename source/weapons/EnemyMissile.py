import arcade
from source.constant import *


class EnemyMissile(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(
            SPRITE_FILE,
            image_x=ENEMY_MISSILE_ORIGIN[0],
            image_y=ENEMY_MISSILE_ORIGIN[1],
            image_width=MISSILE_SPRITE_SIZE,
            image_height=MISSILE_SPRITE_SIZE,
            hit_box_algorithm=None,
            scale=SPRITE_SCALING,
            center_x=x + MISSILE_SPRITE_SIZE,
            center_y=y + MISSILE_SPRITE_SIZE
        )

    def update(self):
        if self.center_y > 0:
            self.center_y -= MISSILE_SPEED
        else:
            self.remove_from_sprite_lists()
