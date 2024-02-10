import os
import random

# os.environ["ARCADE_HEADLESS"] = "True"

import arcade

from source.characters.EnemyList import EnemyList
from source.characters.GalagaBoss import GalagaBoss
from source.characters.Goei import Goei
from source.characters.Zako import Zako
from source.constant import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_LINE, CHAR_SPRITE_SIZE, SPRITE_SCALING, CENTER, \
    SPRITE_SPACING
from source.effect.Star import Star
from source.ui.Agent import Agent, KILL
from source.ui.ScoreBoard import ScoreBoard


class Window(arcade.Window):
    def __init__(self, alpha, gamma, radars):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "HollyGalagia")
        self.__enemy = EnemyList()
        self.__player: Agent = Agent(self.__enemy, radars, alpha, gamma)
        self.__actions: [int] = []
        self.__effects = arcade.SpriteList()
        self.__time = 0
        self.__waiting = self.formation()
        self.__wave = 0
        self.__pause = False
        self.__stars: [Star] = []
        self.__scoreboard = ScoreBoard()

    def setup(self):
        for i in range(100):
            self.__stars.append(Star())

    def start(self):
        self.run()

    def formation(self):
        enter = random.randint(1, 2)
        alt = random.randint(0, 1) == 1
        for i in range(0, 8):
            if i % 2 == 0:
                yield Zako(
                    (self.get_col(-1) if i % 4 == 0 else self.get_col(1)),
                    (self.get_line(1) if i < 4 else self.get_line(0)),
                    self.__scoreboard.level,
                    enter,
                    alt
                )
            else:
                yield Goei(
                    (self.get_col(-1) if i % 4 == 1 else self.get_col(1)),
                    (self.get_line(2) if i > 4 else self.get_line(3)),
                    self.__scoreboard.level,
                    enter,
                    alt
                )
        enter = random.randint(1, 2)
        alt = random.randint(0, 1) == 1
        for i in range(0, 8):
            if i % 2 == 0:
                yield GalagaBoss(
                    self.get_col((1 if i < 4 else 2) * (1 if i % 4 == 0 else -1)),
                    self.get_line(4),
                    self.__scoreboard.level,
                    enter,
                    alt
                )
            else:
                yield Goei(
                    self.get_col(-2 if (i - 1) % 4 == 0 else 2),
                    (self.get_line(2) if i / 4 < 1 else self.get_line(3)),
                    self.__scoreboard.level,
                    enter,
                    alt
                )
        enter = random.randint(1, 2)
        alt = random.randint(0, 1) == 1
        for i in range(0, 8):
            yield Goei(
                self.get_col((3 if i < 4 else 4) * (1 if i % 2 == 0 else -1)),
                (self.get_line(2) if i % 4 < 2 else self.get_line(3)),
                self.__scoreboard.level,
                enter,
                alt
            )
        enter = random.randint(1, 2)
        alt = random.randint(0, 1) == 1
        for i in range(0, 8):
            yield Zako(
                self.get_col((2 if i < 4 else 3) * (1 if i % 2 == 0 else -1)),
                (self.get_line(0) if i % 4 < 2 else self.get_line(1)),
                self.__scoreboard.level,
                enter,
                alt
            )
        enter = random.randint(1, 2)
        alt = random.randint(0, 1) == 1
        for i in range(0, 8):
            yield Zako(
                self.get_col((4 if i < 4 else 5) * (1 if i % 2 == 0 else -1)),
                (self.get_line(0) if i % 4 < 2 else self.get_line(1)),
                self.__scoreboard.level,
                enter,
                alt
            )

    def get_line(self, line: int):
        return BASE_LINE + (CHAR_SPRITE_SIZE + SPRITE_SPACING) * SPRITE_SCALING * line

    def get_col(self, col: int):
        spacing_direction = -1 if col < 0 else 1
        return CENTER - ((CHAR_SPRITE_SIZE + SPRITE_SPACING) * SPRITE_SCALING * spacing_direction / 2) + (CHAR_SPRITE_SIZE + SPRITE_SPACING) * SPRITE_SCALING * col

    def on_update(self, delta_time):
        for s in self.__stars:
            s.on_update()
        if len(self.__actions) > 0:
            if self.__player.killed and 65293 in self.__actions:
                self.__player.revive()
            if self.__pause and 65293 in self.__actions:
                self.__pause = False
            if 65307 in self.__actions:
                self.__player.save()
                self.close()
            moves = list(filter(lambda key: key in [65361, 65363], self.__actions))
            if len(moves) > 0 and moves[-1] == 65361:
                self.__player.move_left()
            elif len(moves) > 0 and moves[-1] == 65363:
                self.__player.move_right(self.width)
            if 32 in self.__actions:
                self.__player.shoot()
            if 101 in self.__actions:
                self.__effects.append(self.__player.explode())
        if self.__pause:
            return
        self.__time += delta_time
        if self.__time > 0.3:
            self.__time = 0
            try:
                if self.__wave == 0 and self.__enemy.total_enemies_spawned < 8:
                    self.__enemy.append(next(self.__waiting))
                elif self.__wave == 1 and self.__enemy.total_enemies_spawned < 16:
                    self.__enemy.append(next(self.__waiting))
                elif self.__wave == 2 and self.__enemy.total_enemies_spawned < 24:
                    self.__enemy.append(next(self.__waiting))
                elif self.__wave == 3 and self.__enemy.total_enemies_spawned < 32:
                    self.__enemy.append(next(self.__waiting))
                elif self.__wave == 4 and self.__enemy.total_enemies_spawned < 40:
                    self.__enemy.append(next(self.__waiting))
                elif self.__wave == 5:
                    self.__enemy.can_attack()
            except StopIteration:
                pass
            if self.__enemy.total_idle() == self.__enemy.total():
                self.__wave += 1
        enemy_killed = self.detect_enemy_hit()
        killed = False
        win_or_loose = None
        if self.__wave >= 5:
            for e in self.__enemy.detect_collision_with_player(self.__player):
                self.__effects.append(e)
                killed = True
        explosion = self.__enemy.detect_hit_with_player(self.__player)
        self.__player.update()
        if explosion is not None:
            killed = True
            self.__effects.append(explosion)
        self.__effects.update()
        self.__enemy.update()
        self.__scoreboard.update()
        if self.__enemy.total_enemies_spawned > 0 and self.__enemy.total() == 0 and self.__wave > 5:
            if self.__scoreboard.level < 256:
                self.__new_level()
            else:
                win_or_loose = True
            # self.__pause = True
        if self.__player.life == 0:
            win_or_loose = False
        if win_or_loose is not None:
            self.__player.save()
        # self.__player.do(killed, enemy_killed, win_or_loose)

    def __new_level(self):
        self.__wave = 0
        self.__enemy = EnemyList()
        self.__scoreboard.next_level()
        self.__waiting = self.formation()

    def on_draw(self):
        self.clear()
        self.__player.draw()
        self.__effects.draw(pixelated=True)
        self.__enemy.draw(pixelated=True)
        for s in self.__stars:
            s.on_draw()
        self.__scoreboard.draw(pixelated=True)

    def on_key_press(self, symbol: int, modifiers: int):
        self.__actions.append(symbol)
        print(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in self.__actions:
            self.__actions.remove(symbol)

    def detect_enemy_hit(self):
        tot = 0
        for m in self.__player.missiles:
            hit_list = arcade.check_for_collision_with_list(m, self.__enemy)
            for enemy in hit_list:
                explosion = enemy.take_damage()
                if explosion is not None:
                    tot += 1
                    self.__scoreboard.score += KILL
                    self.__effects.append(explosion)
                    enemy.remove_from_sprite_lists()
            if len(hit_list) != 0:
                m.remove_from_sprite_lists()
        return tot
