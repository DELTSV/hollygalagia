import arcade

from source.constant import EXPLOSION_SPRITE_SIZE, SPRITE_SCALING


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
        if int(self.__current_texture / 15) < len(self.textures):
            self.set_texture(int(self.__current_texture / 15))
        else:
            self.remove_from_sprite_lists()

