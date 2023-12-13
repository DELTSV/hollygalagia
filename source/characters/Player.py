import arcade

from source.effect.PlayerExplosion import PlayerExplosion
from source.constant import *
from source.weapons.Missile import Missile


class Player:
    def __init__(self):
        self.__x = WINDOW_WIDTH / 2
        self.__y = PLAYER_LINE
        self.__sprite = self.__get_sprite(6)
        self.missiles = arcade.SpriteList()
        self.__delay = 0
        self.__life = 3
        self.__killed = False

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value): self.__x = value

    @property
    def y(self):
        return self.__y

    @property
    def sprite(self):
        return self.__sprite

    @property
    def life(self):
        return self.__life

    @property
    def killed(self):
        return self.__killed

    @killed.setter
    def killed(self, value):
        self.__killed = value

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
        if self.__killed:
            self.__x = -1000
        self.__sprite.center_x = self.__x + CHAR_SPRITE_SIZE * SPRITE_SCALING / 2
        self.__sprite.center_y = self.__y + CHAR_SPRITE_SIZE * SPRITE_SCALING / 2
        self.__sprite.update()
        for m in self.missiles:
            m.update()
        if self.__delay > 0:
            self.__delay -= 1

    def revive(self):
        if self.__life > 0:
            self.__x = WINDOW_WIDTH / 2
            self.__killed = False
            self.__life -= 1

    def draw(self):
        self.__sprite.draw(pixelated=True)
        for m in self.missiles:
            m.draw(pixelated=True)

    def move_left(self):
        if not self.__killed and self.__x > 0:
            self.__x -= PLAYER_SPEED

    def move_right(self, map_max: int):
        if not self.__killed and self.__x < map_max - CHAR_SPRITE_SIZE - PLAYER_SPEED:
            self.__x += PLAYER_SPEED

    def explode(self) -> PlayerExplosion:
        self.__killed = True
        return PlayerExplosion(self.__x, self.__y)

    def shoot(self):
        if not self.__killed and len(self.missiles) < 2 and self.__delay == 0:
            self.missiles.append(Missile(self.__x, self.__y))
            self.__delay = 10
