import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .utils import time
from .path import Path


class Enemy:
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, start_time: float):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.path = Path(start_time, [(100, 0), (100, 300), (SCREEN_WIDTH - 100, 300), (SCREEN_WIDTH - 100, 300), (SCREEN_WIDTH - 100, 0)], 300)
        self.start_time = start_time
        self.visible = False

    def update(self):
        position = self.path.get_position(time() - self.start_time)

        if position is None:
            self.visible = False
        else:
            self.visible = True
            self.rect.center = position

    def render(self, screen: pygame.Surface):
        if self.visible:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)