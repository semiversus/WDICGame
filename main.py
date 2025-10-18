import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000
FRAMES_PER_SECOND = 30


class Manager:
    def __init__(self):
        pygame.init()
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
    def __init__(self, game: Manager):
        self.game = game
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.scene = Game(self.game)
    
    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        font = pygame.font.Font(None, 74)
        text = font.render("WDIC Game", True, (255, 255, 255))
        screen.blit(text, (50, 450))


class Game:
    def __init__(self, manager: Manager):
        self.manager = manager
        self.player = Player(self)
        self.enemies: list[Enemy] = [Enemy(i * 1000) for i in range(5)]
    
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player.x_speed = 1
            elif event.key == pygame.K_LEFT:
                self.player.x_speed = -1
            elif event.key == pygame.K_SPACE:
                self.player.shot()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                self.player.x_speed = 0
    
    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

    def render(self, screen: pygame.Surface):
        self.player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)


class Player:
    WIDTH = 30
    HEIGHT = 30

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
    WIDTH = 3
    HEIGHT = 20
    SPEED = 30

    def __init__(self, x: float):
        self.rect = pygame.Rect(x - self.WIDTH / 2, SCREEN_HEIGHT - 100 - self.HEIGHT / 2, self.WIDTH, self.HEIGHT)
        print(self.rect.centery)

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

class Enemy:
    WIDTH = 30
    HEIGHT = 30

    def __init__(self, time_offset: int):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.path = Path()
        self.start_time = pygame.time.get_ticks() + time_offset
    
    def update(self):
        self.rect.center = self.path.get_position(pygame.time.get_ticks() - self.start_time)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)

class Path:
    def get_position(self, time_elapsed: int) -> tuple[float, float]:
        if time_elapsed < 0:
            return (200, -500)
        elif time_elapsed < 2000:
            x = 200
            y = time_elapsed / 2000 * 200
        elif time_elapsed < 6000:
            x = 200 + (time_elapsed - 2000) / 4000 * (SCREEN_WIDTH - 400)
            y = 200
        else:
            x = SCREEN_WIDTH - 200
            y = 200 - (time_elapsed - 6000) / 4000 * 200

        return (x, y)

Manager().run()