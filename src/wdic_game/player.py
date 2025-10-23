import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game


class Player:
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, game: Game):
        self.game = game
        self.rect = pygame.Rect(500 - self.WIDTH / 2, SCREEN_HEIGHT - 100 - self.HEIGHT / 2, self.WIDTH, self.HEIGHT)
        self.x_speed = 0
        self.missles: list[PlayerMissle] = []

    def shot(self):
        missle = PlayerMissle(self.rect.centerx)
        self.missles.append(missle)

    def update(self):
        self.rect.x += self.x_speed * 20
        self.rect.centerx = max(self.WIDTH / 2, min(self.rect.centerx, SCREEN_WIDTH - self.WIDTH / 2))

        for missle in tuple(self.missles):
            missle.update(self.game)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

        for missle in tuple(self.missles):
            missle.render(screen)


class PlayerMissle:
    WIDTH = 10
    HEIGHT = 25
    SPEED = 30

    def __init__(self, x: float):
        self.rect = pygame.Rect(x - self.WIDTH / 2, SCREEN_HEIGHT - 100 - self.HEIGHT / 2, self.WIDTH, self.HEIGHT)

    def update(self, game: Game):
        self.rect.centery -= self.SPEED
        if self.rect.centery < 0:
            game.player.missles.remove(self)

        for enemy in tuple(game.enemies):
            if self.rect.colliderect(enemy.rect):
                game.enemies.remove(enemy)
                game.player.missles.remove(self)
                break

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
