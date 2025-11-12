import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game
from .utils import get_asset_path


class Player:
    def __init__(self, game: Game):
        self.game = game
        self.image = pygame.image.load(get_asset_path("images/player_ship.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(SCREEN_WIDTH / 2 - self.rect.width / 2, SCREEN_HEIGHT - 100 - self.rect.height / 2)
        self.x_speed = 0
        self.missles: list[PlayerMissle] = []

    def shot(self):
        missle = PlayerMissle(self.rect.centerx)
        self.missles.append(missle)

    def update(self):
        self.rect.x += self.x_speed * 20

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        for missle in tuple(self.missles):
            missle.update(self.game)

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

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
