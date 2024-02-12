import arcade
from source.constant import *


class Missile(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(
            SPRITE_FILE,
            image_x=PLAYER_MISSILE_ORIGIN[0],
            image_y=PLAYER_MISSILE_ORIGIN[1],
            image_width=MISSILE_SPRITE_SIZE,
            image_height=MISSILE_SPRITE_SIZE,
            hit_box_algorithm='Simple',
            scale=SPRITE_SCALING,
            center_x=x + MISSILE_SPRITE_SIZE,
            center_y=y + MISSILE_SPRITE_SIZE
        )

    def update(self):
        if self.center_y > WINDOW_HEIGHT - MISSILE_SPRITE_SIZE / 2:
            self.remove_from_sprite_lists()
        else:
            self.center_y += MISSILE_SPEED
