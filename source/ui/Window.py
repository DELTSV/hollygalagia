from typing import Dict

import arcade

from source.characters.Player import Player
from source.constant import WINDOW_WIDTH, WINDOW_HEIGHT


class Window(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Galaga")
        self.__player: Player | None = None
        self.__actions: [int] = []
        self.__effects = arcade.SpriteList()

    def setup(self):
        self.__player = Player()

    def start(self):
        self.run()

    def on_update(self, delta_time):
        if len(self.__actions) > 0:
            if self.__actions[-1] == 65361:
                self.__player.move_left()
            elif self.__actions[-1] == 65363:
                self.__player.move_right(self.width)
            if 32 in self.__actions:
                self.__player.shoot()
            if 101 in self.__actions:
                self.__effects.append(self.__player.explode())
        self.__player.update()
        self.__effects.update()

    def on_draw(self):
        self.clear()
        self.__player.draw()
        self.__effects.draw(pixelated=True)

    def on_key_press(self, symbol: int, modifiers: int):
        self.__actions.append(symbol)
        print(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        self.__actions.remove(symbol)
