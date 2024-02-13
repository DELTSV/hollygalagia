import json

import arcade

from source.characters import EnemyList
from source.characters.Player import Player
from source.constant import WINDOW_WIDTH, CHAR_SPRITE_SIZE, SPRITE_SCALING, PLAYER_SPEED
from source.ui.Lidar import Lidar
from source.ui.Radar import Radar, STATE
from source.ui.ZoneRadar import ZoneRadar

DEFAULT = -2
KILL = 100
WIN = 1_000
LOOSE = -1_000
OUT_MAP = -1_000
FIRED = 0

MOVE_LEFT = 0
MOVE_RIGHT = 1
FIRE = 2

ACTIONS = [MOVE_LEFT, MOVE_RIGHT, FIRE]


def increment(index: [int], max: int):
    i = 0
    index[i] += 1
    while i < len(index) and index[i] >= max:
        index[i] = 0
        if i < len(index) - 1:
            index[i+1] += 1
        i += 1


def format_radar(radars: [Radar]) -> str:
    return "-".join(["{}_{}".format(r.column, r.line) for r in radars])


class Agent(Player):
    def __init__(self, enemy_list: EnemyList, radar_position: [(int, int)], alpha, gamma):
        super().__init__(enemy_list)
        self.__score = 0
        self.__alpha = alpha
        self.__gamma = gamma
        self.__qtable = {}
        self.__radar = arcade.SpriteList()
        self.__zoneRadar = arcade.SpriteList()
        self.__zoneRadar.append(ZoneRadar(-9, 9, self.x, self.y))
        self.__zoneRadar.append(ZoneRadar(9, 9, self.x, self.y))
        self.__lidar = Lidar(self.x + CHAR_SPRITE_SIZE / 2 * SPRITE_SCALING, self.enemy_list)
        for x, y in radar_position:
            self.__radar.append(Radar(x, y, self.x, self.y))
        tmp = self.load()
        if tmp is None:
            radar_state = []
            index = []
            for c, l in radar_position:
                radars = []
                for s in STATE:
                    radars.append((l, c, s))
                index.append(0)
                radar_state.append(radars)
            done = False
            while not done:
                key = ()
                for i in range(0, len(index)):
                    key += radar_state[i][index[i]]
                for s in STATE:
                    for zr1 in STATE:
                        for zr2 in STATE:
                            for i in range(0, 3):
                                key2 = key + (zr1, zr2, s, i)
                                self.__qtable[key2] = {}
                                for a in ACTIONS:
                                    self.__qtable[key2][a] = 0.0
                increment(index, len(STATE))
                if max(index) == 0:
                    done = True
        else:
            for i in tmp:
                val = {}
                for j in tmp[i]:
                    val[int(j)] = tmp[i][j]
                self.__qtable[i] = val

    def get_best_action(self):
        k = self.get_state()
        action = self.arg_max(self.__qtable[k])
        return action

    def get_state(self):
        return self.get_radar_data() + (self.__lidar.detect_nearest_object(), len(self.missiles))

    def __create_radar_sprite(self, line: int, column: int) -> arcade.Sprite:
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        return arcade.Sprite(
            "resources/box.png",
            SPRITE_SCALING,
            image_width=CHAR_SPRITE_SIZE,
            image_height=CHAR_SPRITE_SIZE,
            center_x=(column * size + size / 2) + self.x,
            center_y=(line * size + size / 2) + self.y
        )

    def get_radar_data(self):
        data = ()
        missiles = []
        for e in self.enemy_list:
            missiles.append(e.missiles)
        for r in self.__radar:
            data += r.get_data(self.enemy_list, missiles)
        for z in self.__zoneRadar:
            data += z.get_data(self.enemy_list, missiles)
        return data

    def get_enemy_in_square_from_user(self, line: int, column: int):
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        target = arcade.Sprite("resources/box.png", SPRITE_SCALING, image_width=size, image_height=size, center_x=line * size - size / 2, center_y=column * size - size / 2)
        return len(arcade.check_for_collision_with_list(target, self.enemy_list)) != 0

    def move_left(self) -> bool:
        can_move = super().move_left()
        if can_move:
            for s in self.__radar:
                s.center_x -= PLAYER_SPEED
            for s in self.__zoneRadar:
                s.center_x -= PLAYER_SPEED
            self.__lidar.x -= PLAYER_SPEED
        return can_move

    def move_right(self, map_max: int) -> bool:
        can_move = super().move_right(map_max)
        if can_move:
            for s in self.__radar:
                s.center_x += PLAYER_SPEED
            for s in self.__zoneRadar:
                s.center_x += PLAYER_SPEED
            self.__lidar.x += PLAYER_SPEED
        return can_move

    def update(self):
        super().update()
        if not self.killed:
            self.__radar.update()
            self.__zoneRadar.update()

    def draw(self):
        super().draw()
        if not self.killed:
            self.__radar.draw()
            self.__zoneRadar.draw()
            self.__lidar.draw()

    def arg_max(self, table):
        return max(table, key=table.get)

    def do(self, killed: bool, enemy_killed: int, win_or_loose: bool | None):
        action = self.get_best_action()
        reward = DEFAULT
        old_state = self.get_state()
        if action == MOVE_LEFT:
            if not self.move_left():
                reward += OUT_MAP
        if action == MOVE_RIGHT:
            if not self.move_right(WINDOW_WIDTH):
                reward += OUT_MAP
        if action == FIRE:
            reward += FIRED
            self.shoot()
        if killed:
            reward += LOOSE
            self.revive()
        reward += KILL * enemy_killed
        if win_or_loose is not None:
            if win_or_loose:
                reward += WIN
            else:
                reward += LOOSE
        current = self.__qtable[old_state][action]
        next_max = self.arg_max(self.__qtable[self.get_state()])
        self.__score += reward
        self.__qtable[old_state][action] = current + self.__alpha * (reward + self.__gamma * next_max - current)
        return reward

    def save(self):
        filename = "./qtable-{}-{}-{}".format(self.__alpha, self.__gamma, format_radar(self.__radar))
        with open(filename, 'w') as f:
            list = {}
            for k, v in self.__qtable.items():
                list[k.__str__()] = v
            f.write(json.dumps(list))

    def load(self):
        filename = "./qtable-{}-{}-{}".format(self.__alpha, self.__gamma, format_radar(self.__radar))
        try:
            with open(filename, "r") as f:
                tmp = json.loads(f.read())
                final = {}
                for k, v in tmp.items():
                    k_items = k.removeprefix("(").removesuffix(")").split(",")
                    for i in range(0, len(k_items)):
                        k_items[i] = int(k_items[i])
                    new_k = tuple(k_items)
                    final[new_k] = v
                return final
        except FileNotFoundError:
            return None

    def revive(self):
        super().revive()
        self.__lidar.x = self.x + CHAR_SPRITE_SIZE / 2 * SPRITE_SCALING
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        for r in self.__radar:
            r.center_x = (r.column * size + size / 2) + self.x

    @property
    def score(self):
        return self.__score
