import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .utils import time
from .path import Path, build_dive_path


class Enemy:
    def __init__(self, path: Path):
        self.rect = pygame.Rect(0, 0, 64, 53)
        self.path = path
        self.visible = False

    def update(self, game: 'Game'):
        position = self.path.get_position(time())

        if self.path.is_finished(time()):
            game.enemies.remove(self)

        if position is None:
            self.visible = False
        else:
            self.visible = True
            self.rect.center = position

    def render(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)


def build_first_wave() -> list[Enemy]:
    return [Enemy(build_dive_path(i)) for i in range(5)]


def build_second_wave() -> list[Enemy]:
    return [Enemy(build_dive_path(i, depth=300 + i * 50, width=50 + i * 100, speed=250)) for i in range(5)]


def build_third_wave() -> list[Enemy]:
    return [Enemy(Path(time() + i, [(100 + (SCREEN_WIDTH - 200) / 8 * i, -100), (100 + (SCREEN_WIDTH - 200) / 8 * i, SCREEN_HEIGHT + 100)], 200)) for i in range(10)]


WAVES = {
    0: build_first_wave,
    1: build_second_wave,
    2: build_third_wave
}


def load_enemy_wave(wave: int) -> list[Enemy]:
    if wave in WAVES:
        return WAVES[wave]()
    
    return []






