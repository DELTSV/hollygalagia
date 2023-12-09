import arcade

from source.characters.PlayerExplosion import PlayerExplosion
from source.constant import *
from source.weapons.Missile import Missile


class Player:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__sprite = self.__get_sprite(6)
        self.missiles = arcade.SpriteList()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value): self.__x = value

    @property
    def y(self):
        return self.__y

    def roll(self):
        pass

    def __get_sprite(self, rotation: int) -> arcade.Sprite:
        return arcade.Sprite(
            SPRITE_FILE,
            image_x=PLAYER_SPRITE_ORIGIN[0] + 18 * rotation,
            image_y=PLAYER_SPRITE_ORIGIN[1],
            image_width=CHAR_SPRITE_SIZE,
            image_height=CHAR_SPRITE_SIZE,
            hit_box_algorithm=None,
            scale=SPRITE_SCALING
        )

    def update(self):
        self.__sprite.center_x = self.__x + CHAR_SPRITE_SIZE * SPRITE_SCALING / 2
        self.__sprite.center_y = self.__y + CHAR_SPRITE_SIZE * SPRITE_SCALING / 2
        self.__sprite.update()
        for m in self.missiles:
            m.update()

    def draw(self):
        self.__sprite.draw(pixelated=True)
        for m in self.missiles:
            m.draw(pixelated=True)

    def move_left(self):
        if self.__x > 0:
            self.__x -= PLAYER_SPEED

    def move_right(self, map_max: int):
        if self.__x < map_max - CHAR_SPRITE_SIZE - PLAYER_SPEED:
            self.__x += PLAYER_SPEED

    def explode(self) -> PlayerExplosion:
        return PlayerExplosion(self.__x, self.__y)

    def shoot(self):
        print(len(self.missiles))
        if len(self.missiles) < 8:
            self.missiles.append(Missile(self.__x, self.__y))
