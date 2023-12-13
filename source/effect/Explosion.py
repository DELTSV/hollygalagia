import arcade

from source.constant import *


class Explosion(arcade.Sprite):

    def __init__(self, texture_list, x, y):
        super().__init__()
        self.center_x = x + EXPLOSION_SPRITE_SIZE / 2
        self.center_y = y + EXPLOSION_SPRITE_SIZE / 2
        self.__current_texture = 0
        self.textures = texture_list
        self.scale = SPRITE_SCALING

    def update(self):
        self.__current_texture += 1
        if int(self.__current_texture / EXPLOSION_SPEED) < len(self.textures):
            self.set_texture(int(self.__current_texture / EXPLOSION_SPEED))
            return True
        else:
            self.remove_from_sprite_lists()
            return False

