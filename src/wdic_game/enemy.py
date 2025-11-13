import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .utils import time
from .path import Path


class Enemy:
    def __init__(self, path: Path):
        self.rect = pygame.Rect(0, 0, 64, 53)
        self.path = path
        self.visible = False

    def update(self, game: 'Game'):
        position = self.path.get_position(time())

        if self.path.is_finished(time()):
            game.enemies.remove(self)
            return

        if position is None:
            self.visible = False
        else:
            self.visible = True
            self.rect.center = position

    def render(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
