import arcade

from source.constant import SPRITE_SCALING, CHAR_SPRITE_SIZE, WINDOW_WIDTH
from source.ui.Radar import EMPTY, COLLIDED


class ZoneRadar(arcade.Sprite):
    def __init__(self, column, line, x, y):
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        super().__init__(
            "resources/zoneBox.png",
            SPRITE_SCALING,
            image_width=270,
            image_height=128,
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
        if enemy or missile:
            return tuple([COLLIDED])
        return tuple([EMPTY])

    @property
    def line(self):
        return self.__line

    @property
    def column(self):
        return self.__column
