import arcade

from source.characters.GalagaBoss import GalagaBoss
from source.characters.Player import Player
from source.constant import WINDOW_WIDTH, WINDOW_HEIGHT


class Window(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Galaga")
        self.__player: Player | None = None
        self.__actions: [int] = []
        self.__effects = arcade.SpriteList()
        self.__enemy = arcade.SpriteList()

    def setup(self):
        self.__player = Player()
        self.__enemy.append(GalagaBoss(150, 500))

    def start(self):
        self.run()

    def on_update(self, delta_time):
        if len(self.__actions) > 0:
            moves = list(filter(lambda key: key in [65361, 65363], self.__actions))
            if len(moves) > 0 and moves[-1] == 65361:
                self.__player.move_left()
            elif len(moves) > 0 and moves[-1] == 65363:
                self.__player.move_right(self.width)
            if 32 in self.__actions:
                self.__player.shoot()
            if 101 in self.__actions:
                self.__effects.append(self.__player.explode())
        self.detect_enemy_hit()
        self.__player.update()
        self.__effects.update()
        self.__enemy.on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.__player.draw()
        self.__effects.draw(pixelated=True)
        self.__enemy.draw(pixelated=True)

    def on_key_press(self, symbol: int, modifiers: int):
        self.__actions.append(symbol)
        print(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in self.__actions:
            self.__actions.remove(symbol)

    def detect_enemy_hit(self):
        for m in self.__player.missiles:
            hit_list = arcade.check_for_collision_with_list(m, self.__enemy)
            for enemy in hit_list:
                explosion = enemy.take_damage()
                if explosion is not None:
                    self.__effects.append(explosion)
                    enemy.remove_from_sprite_lists()
            if len(hit_list) != 0:
                m.remove_from_sprite_lists()
