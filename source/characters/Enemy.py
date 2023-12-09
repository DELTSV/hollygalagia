import arcade

from source.constant import *
from source.effect.EnemyExplosion import EnemyExplosion


class Enemy(arcade.Sprite):
    def __init__(self, x: int, y: int, texture_list):
        self.__state_delay = 0
        self.__state = 0
        self.orientation = 0
        super().__init__(
            scale=SPRITE_SCALING,
            center_x=x,
            center_y=y,
            hit_box_algorithm='Simple'
        )
        self.textures = texture_list

    def take_damage(self):
        return self.explode()

    def explode(self):
        return EnemyExplosion(int(self.center_x), int(self.center_y))

    def on_update(self, delta_time: float = 1 / 60):
        self.orientation = (self.orientation + 1) % 360
        self.center_x += 1
        self.__state_delay += delta_time
        if self.__state_delay > 1:
            self.__state = (self.__state + 1) % 2
            self.__state_delay = 0
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

