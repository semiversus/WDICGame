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
        self.game_over = False

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
        if self.game_over:
            return

        self.player.update(self)
    
        for enemy in list(self.enemies):
            enemy.update(self)

            # 🚨 PLAYER COLLISION CHECK
            if enemy.visible and enemy.rect.colliderect(self.player.rect):
                print("GAME OVER – You were hit!")
                self.game_over = True
                return  # stop update()
        
        # Falls alle Gegner weg: nächste Welle
        if not self.enemies:
            self.enemy_wave_index += 1
            self.enemies = load_enemy_wave(self.enemy_wave_index)


    def render(self, screen: pygame.Surface):
        self.player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)

        if self.game_over:
            font = pygame.font.SysFont("Arial", 48)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(400, 300))

            # Schwarzer Hintergrund für den Text
            bg_rect = rect.inflate(20, 20)  # 10px Rand außen rum
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)

            # Roten Rahmen um das Rechteck
            pygame.draw.rect(screen, (255, 0, 0), bg_rect, 3)  # 3 px dick

            # Text drauf
            screen.blit(text, rect)
