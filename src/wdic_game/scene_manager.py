import pygame

from .consts import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMES_PER_SECOND


class SceneManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("WDIC Game")

        self.scene = StartScene(self)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.HWSURFACE)

        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):
        while self.running:
            self.scene.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.scene.render(self.screen)
            pygame.display.update()

            self.clock.tick(FRAMES_PER_SECOND)


class StartScene:
    def __init__(self, manager: SceneManager):
        self.manager = manager

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            from .game import Game
            self.manager.scene = Game(self.manager)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        font = pygame.font.Font(None, 74)
        text = font.render("WDIC Game", True, (255, 255, 255))
        text.get_rect()
        screen.blit(text, (70, 470))
