import arcade

from source.constant import SPRITE_SCALING, CHAR_SPRITE_SIZE

EMPTY = 0
ENEMY = 1
MISSILE = 2
ENEMY_AND_MISSILE = 3

STATE = [EMPTY, ENEMY, MISSILE, ENEMY_AND_MISSILE]


class Radar(arcade.Sprite):
    def __init__(self, column, line, x, y):
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        super().__init__(
            "resources/box.png",
            SPRITE_SCALING,
            image_width=CHAR_SPRITE_SIZE,
            image_height=CHAR_SPRITE_SIZE,
            center_x=(column * size + size / 2) + x,
            center_y=(line * size + size / 2) + y
        )
        self.__line = line
        self.__column = column

    def get_data(self, enemies, missiles) -> tuple:
        enemy_collisions = arcade.check_for_collision_with_list(self, enemies)
        missile_collision = arcade.check_for_collision_with_lists(self, missiles)
        enemy = len(enemy_collisions) > 0
        missile = len(missile_collision) > 0
        if enemy and missile:
            return self.__line, self.column, ENEMY_AND_MISSILE
        elif enemy:
            return self.__line, self.column, ENEMY
        elif missile:
            return self.__line, self.column, MISSILE
        return self.__line, self.column, EMPTY

    @property
    def line(self):
        return self.__line

    @property
    def column(self):
        return self.__column
