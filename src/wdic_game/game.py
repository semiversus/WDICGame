import pygame

from .scene_manager import SceneManager
from .enemy_wave import load_enemy_wave


class Game:
    def __init__(self, manager: SceneManager):
        from .player import Player
        from .enemy import Enemy

        self.manager = manager
        self.score = 0
        self.player = Player()
        self.enemy_wave_index = 0
        self.enemies: list[Enemy] = load_enemy_wave(self.enemy_wave_index)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player.x_speed = 1
            elif event.key == pygame.K_LEFT:
                self.player.x_speed = -1
            elif event.key == pygame.K_SPACE:
                self.player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                self.player.x_speed = 0

    def update(self):
        self.player.update(self)
        for enemy in self.enemies:
            enemy.update(self)
        
        if not self.enemies:
            self.enemy_wave_index += 1
            self.enemies = load_enemy_wave(self.enemy_wave_index)

    def render(self, screen: pygame.Surface):
        self.player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)