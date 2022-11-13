import pygame
from pygame.draw import *
from random import *
from numpy import sin, pi

pygame.init()


class Ball:
    """Game`s main object"""
    def __init__(self, position, radius, color, screen, velocity):
        self.pos = pygame.Vector2(position)
        self.r = radius
        self.color = color
        self.screen = screen
        self.v = pygame.Vector2(velocity)
        self.caught = self.is_caught(None)
        if not self.caught:
            self.draw()

    @property
    def point(self):
        if self.r in range(10, 20):
            return 15
        elif self.r in range(20, 40):
            return 10
        else:
            return 5

    """Object`s moving function"""
    def move(self):
        if not self.caught:
            self.draw()
            self.pos = self.pos + self.v
            if self.pos.x < self.r:
                self.pos.x = self.r
                self.v = pygame.Vector2(-self.v.x, self.v.y)
            elif self.pos.x > Game.WIDTH - self.r:
                self.pos.x = Game.WIDTH - self.r
                self.v = pygame.Vector2(-self.v.x, self.v.y)
            if self.pos.y < self.r:
                self.pos.y = self.r
                self.v = pygame.Vector2(self.v.x, -self.v.y)
            elif self.pos.y > Game.HEIGHT - self.r:
                self.pos.y = Game.HEIGHT - self.r
                self.v = pygame.Vector2(self.v.x, -self.v.y)

    """Appearance of the object"""
    def draw(self):
        circle(surface=self.screen, center=self.pos, radius=self.r, color=self.color)

    """Check if object caught"""
    def is_caught(self, event):
        if event and (self.pos.x - event.pos[0])**2 + (self.pos.y - event.pos[1])**2 <= self.r**2:
            return True
        return False


class WavingBall(Ball):
    """Specific object with changing size"""
    def __init__(self, position, radius, color, screen, velocity, acceleration):
        super().__init__(position, radius, color, screen, velocity)
        self.a = pygame.Vector2(acceleration)
        self.r_0 = radius

    @property
    def point(self):
        if self.r in range(0, 20):
            return 35
        elif self.r in range(20, 40):
            return 25
        else:
            return 15

    def move(self):
        t = pygame.time.get_ticks()
        self.r = self.r_0*(1.5+sin(t*pi/625))
        super().move()


class Game:
    """Game loop class"""
    HEIGHT = 600
    WIDTH = 900
    FPS = 60
    FONT = pygame.font.Font(None, 36)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
    N = 10

    def __init__(self, title):
        self.sc = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.clock = pygame.time.Clock()
        self.balls = []
        pygame.display.set_caption(title)

    def main(self):
        """Project setup function, events` checker, game process"""
        finished = False
        balls = [Ball((randint(50, Game.WIDTH), randint(50, Game.HEIGHT)), randint(10, 50), Game.COLORS[randint(0, 5)],
                      self.sc, (randint(2, 7), randint(2, 7))) for _ in range(Game.N)] + \
                [WavingBall((100, 100), randint(10, 50), Game.COLORS[randint(0, 5)], self.sc,
                            (randint(2, 7), randint(2, 7)), (randint(1, 3), randint(1, 3))) for _ in range(Game.N)]
        points = 0
        while not finished:
            text = Game.FONT.render(f'Score: {str(points)}', True, Game.BLACK)
            self.sc.blit(text, (10, 10))
            self.clock.tick(Game.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                    finished = not finished
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and any(balls):
                    for i in balls:
                        i.caught = i.is_caught(event)
                        if i.caught:
                            balls.remove(i)
                            points += i.point
            for j in balls:
                j.move()
            if not any(balls):
                win_text = Game.FONT.render('YOU WON!!!', True, Game.BLUE)
                self.sc.blit(win_text, (Game.WIDTH/2-50, 10))
            pygame.display.update()
            self.sc.fill(Game.WHITE)
        pygame.quit()


new_game = Game('Pygame Project')
new_game.main()
