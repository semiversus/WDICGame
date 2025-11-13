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
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.player.x_speed = 0  # cancel out
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player.x_speed = 1
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player.x_speed = -1
            else:
                self.player.x_speed = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.shot()
            
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