import arcade

from source.constant import SPRITE_FILE, LITTLE_BADGE_WIDTH, LARGE_BADGE_WIDTH, BADGE_HEIGHT, SPRITE_SCALING, \
    BADGE_ORIGIN, WINDOW_WIDTH, TEXT_SIZE
from source.ui.Char import Char


class ScoreBoard(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.__level = 1
        self.__fifty = 0
        self.__thirty = False
        self.__twenty = False
        self.__ten = False
        self.__five = False
        self.__one = 1
        self.__score = 0
        self.display_badges()
        self.display_score()

    def next_level(self):
        self.__level += 1
        lvl = self.__level
        self.__fifty = int(lvl / 50)
        lvl -= 50 * self.__fifty
        self.__thirty = lvl >= 30
        if self.__thirty:
            lvl -= 30
        self.__twenty = lvl >= 20
        if self.__twenty:
            lvl -= 20
        self.__ten = lvl >= 10
        if self.__ten:
            lvl -= 10
        self.__five = lvl >= 5
        if self.__five:
            lvl -= 5
        self.__one = lvl
        self.display_badges()
        self.display_score()

    def display_badges(self):
        self.clear()
        x = WINDOW_WIDTH
        y = BADGE_HEIGHT * SPRITE_SCALING
        for i in range(self.__one):
            x -= LITTLE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_one(x, y))
        if self.__five:
            x -= LITTLE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_five(x, y))
        if self.__ten:
            x -= LARGE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_ten(x, y))
        if self.__twenty:
            x -= LARGE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_twenty(x, y))
        if self.__thirty:
            x -= LARGE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_thirty(x, y))
        for i in range(self.__fifty):
            x -= LARGE_BADGE_WIDTH * SPRITE_SCALING
            self.append(self.__load_fifty(x, y))

    def display_score(self):
        score = self.__score
        x = WINDOW_WIDTH - (TEXT_SIZE * SPRITE_SCALING)
        y = 100
        if score == 0:
            self.append(Char(0, x, y))
            self.append(Char(0, x - TEXT_SIZE * SPRITE_SCALING, y))
        else:
            negative = False
            if score < 0:
                score = -score
                negative = True
            while score > 0:
                self.append(Char(score % 10, x, y))
                x -= TEXT_SIZE * SPRITE_SCALING
                score //= 10
            if negative:
                self.append(Char(36, x, y))

    def __load_fifty(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0] + 74, BADGE_ORIGIN[1], True, x, y)

    def __load_thirty(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0] + 56, BADGE_ORIGIN[1], True, x, y)

    def __load_twenty(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0] + 38, BADGE_ORIGIN[1], True, x, y)

    def __load_ten(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0] + 20, BADGE_ORIGIN[1], True, x, y)

    def __load_five(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0] + 10, BADGE_ORIGIN[1], False, x, y)

    def __load_one(self, x: int, y: int):
        return self.__load_badges(BADGE_ORIGIN[0], BADGE_ORIGIN[1], False, x, y)


    def __load_badges(self, x: int, y: int, large: bool, center_x: int, center_y: int):
        return arcade.Sprite(
            SPRITE_FILE,
            image_x=x,
            image_y=y,
            image_width=LARGE_BADGE_WIDTH if large else LITTLE_BADGE_WIDTH,
            image_height=BADGE_HEIGHT,
            hit_box_algorithm=None,
            scale=SPRITE_SCALING,
            center_x=center_x,
            center_y=center_y
        )

    @property
    def level(self):
        return self.__level

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score: int):
        self.__score = score
        self.display_score()
