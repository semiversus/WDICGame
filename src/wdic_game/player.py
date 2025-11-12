import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT
from .game import Game
from .utils import get_asset_path


class Player:
    def __init__(self, game: Game):
        self.game = game
        self.image = pygame.image.load(get_asset_path("images/player_ship.png")).convert_alpha()
        self.sound_shoot = pygame.mixer.Sound(get_asset_path("sounds/player_shoot.wav"))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(SCREEN_WIDTH / 2 - self.rect.width / 2, SCREEN_HEIGHT - 100 - self.rect.height / 2)
        self.x_speed = 0
        self.missiles: list[PlayerMissile] = []

    def shoot(self):
        missile = PlayerMissile(self.rect.centerx)
        self.sound_shoot.play()
        self.missiles.append(missile)

    def update(self):
        self.rect.x += self.x_speed * 20

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        for missile in tuple(self.missiles):
            missile.update(self.game)

    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

        for missile in tuple(self.missiles):
            missile.render(screen)


class PlayerMissile:
    SPEED = 20

    def __init__(self, x: float):
        self.rect = pygame.Rect(0, 0, 4, 26)
        self.rect = self.rect.move(x - self.rect.width / 2, SCREEN_HEIGHT - 100 - self.rect.height / 2)

    def update(self, game: Game):
        self.rect.centery -= self.SPEED
        if self.rect.centery < 0:
            game.player.missiles.remove(self)

        for enemy in tuple(game.enemies):
            if self.rect.colliderect(enemy.rect):
                game.enemies.remove(enemy)
                game.player.missiles.remove(self)
                break

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 255), self.rect)
