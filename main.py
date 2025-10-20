import pygame
import math

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FRAMES_PER_SECOND = 30


def time():
    return pygame.time.get_ticks() / 1000.0


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
        self.enemies: list[Enemy] = [Enemy(i + time()) for i in range(5)]

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

class Path:
    def __init__(self, start_time: float, points: list[tuple[float, float]], speed: float):
        self.start_time = start_time
        self.points = points
        self.speed = speed
        self.segment_lengths = []
        self.cumulative_lengths = [0.0]

        for i in range(len(points) - 1):
            dx = points[i + 1][0] - points[i][0]
            dy = points[i + 1][1] - points[i][1]
            seg_length = math.sqrt(dx**2 + dy**2)
            self.segment_lengths.append(seg_length)
            self.cumulative_lengths.append(self.cumulative_lengths[-1] + seg_length)

        self.total_length = self.cumulative_lengths[-1]

    def get_position(self, time: float) -> tuple[float, float]:
        if time < 0:
            return None

        distance = self.speed * time
        if distance >= self.total_length:
            return None

        # Find the segment
        for i in range(len(self.segment_lengths)):
            if distance <= self.cumulative_lengths[i + 1]:
                dist_into_seg = distance - self.cumulative_lengths[i]
                fraction = dist_into_seg / self.segment_lengths[i]
                p1 = self.points[i]
                p2 = self.points[i + 1]
                x = p1[0] + fraction * (p2[0] - p1[0])
                y = p1[1] + fraction * (p2[1] - p1[1])
                return (x, y)

        return self.points[-1]

Manager().run()