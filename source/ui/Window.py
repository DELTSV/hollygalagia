import arcade

from source.characters.GalagaBoss import GalagaBoss
from source.characters.Goei import Goei
from source.characters.Player import Player
from source.characters.Zako import Zako
from source.constant import WINDOW_WIDTH, WINDOW_HEIGHT


class Window(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Galaga")
        self.__player: Player | None = None
        self.__actions: [int] = []
        self.__effects = arcade.SpriteList()
        self.__enemy = arcade.SpriteList()
        self.__time = 0
        self.test = 0
        self.__waiting = self.formation()


    def setup(self):
        self.__player = Player()

    def start(self):
        self.run()

    def formation(self):
        for i in range(0, 4):
            yield Zako(
                WINDOW_WIDTH / 2 - (20 if i % 2 == 0 else -20),
                (450 if i / 2 < 1 else 490),
                1,
                True
            )
            yield Goei(
                WINDOW_WIDTH / 2 - (20 if i % 2 == 0 else -20),
                (530 if i / 2 < 1 else 570),
                1,
                False
            )
        for i in range(0, 8):
            if i % 2 == 0:
                yield GalagaBoss(
                    WINDOW_WIDTH / 2 - (20 if i < 4 else 60) * (1 if i % 4 == 0 else -1),
                    610,
                    1,
                    False
                )
            else:
                yield Goei(
                    WINDOW_WIDTH / 2 - 60 * (1 if (i - 1) % 4 == 0 else -1),
                    (530 if i / 4 < 1 else 570),
                    1,
                    False
                )
        for i in range(0, 8):
            yield Goei(
                WINDOW_WIDTH / 2 - (100 if i < 4 else 140) * (1 if i % 2 == 0 else -1),
                (530 if i % 4 < 2 else 570),
                1,
                False
            )
        for i in range(0, 8):
            yield Zako(
                WINDOW_WIDTH / 2 - (60 if i < 4 else 100) * (1 if i % 2 == 0 else -1),
                (450 if i % 4 < 2 else 490),
                1,
                False
            )
        for i in range(0, 8):
            yield Zako(
                WINDOW_WIDTH / 2 - (140 if i < 4 else 180) * (1 if i % 2 == 0 else -1),
                (450 if i % 4 < 2 else 490),
                1,
                False
            )

    def on_update(self, delta_time):
        self.__time += delta_time
        if self.__time > 0.3:
            self.__time = 0
            try:
                if len(self.__enemy) < 8:
                    self.__enemy.append(next(self.__waiting))
                    self.__enemy.append(next(self.__waiting))
                elif len(self.__enemy) < 16:
                    if self.__enemy[7].is_idle:
                        self.__enemy.append(next(self.__waiting))
                elif len(self.__enemy) < 24:
                    if self.__enemy[15].is_idle:
                        self.__enemy.append(next(self.__waiting))
                elif len(self.__enemy) < 32:
                    if self.__enemy[23].is_idle:
                        self.__enemy.append(next(self.__waiting))
                elif len(self.__enemy) < 40:
                    if self.__enemy[31].is_idle:
                        self.__enemy.append(next(self.__waiting))
            except StopIteration:
                pass
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
        self.__enemy.update()

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
