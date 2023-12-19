import arcade
from arcade.sprite_list.sprite_list import _SpriteType

from source.characters.Enemy import Enemy
from source.characters.Player import Player
from source.effect.Explosion import Explosion
from source.effect.PlayerExplosion import PlayerExplosion


class EnemyList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.__enemies: [Enemy] = []
        self.__total_enemies_spawned: int = 0

    def append(self, sprite: Enemy):
        super().append(sprite)
        self.__total_enemies_spawned += 1
        self.__enemies.append(sprite)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for e in self.__enemies:
            e.draw(filter=filter, pixelated=pixelated, blend_function=blend_function)

    def update(self):
        for e in self.__enemies:
            e.update()

    def remove(self, sprite: _SpriteType):
        super().remove(sprite)
        self.__enemies.remove(sprite)

    def detect_hit_with_player(self, player: Player) -> PlayerExplosion | None:
        for e in self.__enemies:
            explosion = e.detect_missile_hit_player(player)
            if explosion is not None:
                return explosion
        return None

    def detect_collision_with_player(self, player: Player) -> [Explosion]:
        hit_list = arcade.check_for_collision_with_list(player.sprite, self)
        explosion = []
        for e in hit_list:
            explosion.append(e.explode())
            e.remove_from_sprite_lists()
        if len(explosion) > 0:
            explosion.append(player.explode())
        return explosion

    def total_idle(self) -> int:
        return sum(e.is_idle for e in self.__enemies)

    def total(self) -> int:
        return len(self.__enemies)

    @property
    def total_enemies_spawned(self) -> int:
        return self.__total_enemies_spawned

    def can_attack(self):
        for e in self.__enemies:
            e.can_attack = True
