import json

from source.characters import EnemyList
from source.characters.Player import Player
from source.constant import WINDOW_WIDTH, CHAR_SPRITE_SIZE, SPRITE_SCALING

KILL = 100
DEATH = -1_000
WIN = 10_000
LOOSE = -10_000
OUT_MAP = -1_000

MOVE_LEFT = 0
MOVE_RIGHT = 1
FIRE = 2

ACTIONS = [MOVE_LEFT, MOVE_RIGHT, FIRE]


class Agent(Player):
    def __init__(self, enemy_list: EnemyList):
        super().__init__(enemy_list)
        self.__score = -1
        self.__qtable = {}
        tmp = self.load()
        if tmp is None:
            for e1 in range(-1, 3):
                for e2 in range(-1, 3):
                    k = (e1, e2)
                    self.__qtable[k] = {}
                    for action in ACTIONS:
                        self.__qtable[k][action] = 0.0
        else:
            for i in tmp:
                val = {}
                for j in tmp[i]:
                    val[int(j)] = tmp[i][j]
                self.__qtable[i] = val

    def get_best_action(self):
        l = self.get_left_enemy()
        r = self.get_right_enemy()
        k = (l, r)
        action = self.arg_max(self.__qtable[k])
        return action

    def get_left_enemy(self) -> int:
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        enemy = []
        for e in self.enemy_list:
            if 0 < e.center_y < size:
                if e.center_x < self.sprite.center_x and self.sprite.center_x - e.center_x < 100:
                    enemy.append(int((self.sprite.center_x - e.center_x) / 33.3))
        if len(enemy) == 0:
            return -1
        return min(enemy)

    def get_right_enemy(self) -> int:
        size = CHAR_SPRITE_SIZE * SPRITE_SCALING
        enemy = []
        for e in self.enemy_list:
            if 0 < e.center_y < size:
                if e.center_x > self.sprite.center_x and e.center_x - self.sprite.center_x < 100:
                    enemy.append(int((e.center_x - self.sprite.center_x) / 33.3))
        if len(enemy) == 0:
            return -1
        return min(enemy)

    def arg_max(self, table):
        return max(table, key=table.get)

    def do(self, killed: bool, enemy_killed: int, win_or_loose: bool | None):
        action = self.get_best_action()
        reward = 0
        old_state = (self.get_left_enemy(), self.get_right_enemy())
        if action == MOVE_LEFT:
            if not self.move_left():
                reward += OUT_MAP
        if action == MOVE_RIGHT:
            if not self.move_right(WINDOW_WIDTH):
                reward += OUT_MAP
        if action == FIRE:
            self.shoot()
        if killed:
            reward += DEATH
            self.revive()
        reward += KILL * enemy_killed
        if win_or_loose is not None:
            if win_or_loose:
                reward += WIN
            else:
                reward += LOOSE
        current = self.__qtable[old_state][action]
        alpha = 0.5
        gamma = 0.5
        next_max = self.arg_max(self.__qtable[(self.get_left_enemy(), self.get_right_enemy())])
        self.__score += reward
        self.__qtable[old_state][action] = current + alpha * (reward + gamma * next_max - current)

    def save(self):
        with open("./qtable", 'w') as f:
            list = {}
            for k, v in self.__qtable.items():
                list[k.__str__()] = v
            f.write(json.dumps(list))

    def load(self):
        try:
            with open("./qtable", "r") as f:
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
