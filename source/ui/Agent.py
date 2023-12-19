import json

from source.characters.Player import Player
from source.constant import WINDOW_WIDTH

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
    def __init__(self):
        super().__init__()
        self.__score = -1
        self.__qtable = {}
        tmp = self.load()
        if tmp is None:
            for x in range(0, WINDOW_WIDTH):
                self.__qtable[x] = {}
                for action in ACTIONS:
                    self.__qtable[x][action] = 0.0
        else:
            for i in tmp:
                val = {}
                for j in tmp[i]:
                    val[int(j)] = tmp[i][j]
                self.__qtable[int(i)] = val

    def get_best_action(self):
        action = self.arg_max(self.__qtable[self.x])
        return action

    def arg_max(self, table):
        return max(table, key=table.get)

    def do(self, killed: bool, enemy_killed: int, win_or_loose: bool | None):
        action = self.get_best_action()
        reward = 0
        print(self.__qtable[self.x])
        old_state = self.x
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
        alpha = 1
        gamma = 0.5
        next_max = self.arg_max(self.__qtable[self.x])
        self.__score += reward
        self.__qtable[old_state][action] = current + alpha * (reward + gamma * next_max - current)

    def save(self):
        with open("./qtable", 'w') as f:
            f.write(json.dumps(self.__qtable))

    def load(self):
        try:
            with open("./qtable", "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None
