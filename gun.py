import math
from random import choice, randint
import pygame

pygame.init()

f1 = pygame.font.Font(None, 24)
f2 = pygame.font.Font(None, 48)

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1

    def move(self):
        """
        Движение шарика
        """
        self.y += self.vy
        self.x += self.vx
        if self.x + self.vx >= WIDTH - 50:
            self.vx *= -1
        if self.x + self.vx <= 50:
            self.vx *= -1
        if self.y <= -self.r:
            self.live = 0

    def draw(self):
        """
        Отрисовка шарика
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            self.r)

    def hittest(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        x2, y2 = obj.x, obj.y
        if (self.x - x2) ** 2 + (self.y - y2) ** 2 <= (self.r + obj.r) ** 2:
            self.color = (255, 0, 0)
            self.r = 30
            self.live = 0
            return True
        return False


class Gun:
    def __init__(self, screen):
        """
        Конструктор класса Gun
        """
        self.an = None
        self.x = WIDTH / 2
        self.y = HEIGHT - 20
        self.r = 10
        self.vx = 4
        self.live = 1
        self.color = (200, 0, 200)
        self.screen = screen

    def move_right(self):
        """
        Движение пушки-танка вправо
        """
        if self.x <= 750:
            self.x += self.vx

    def move_left(self):
        """
        Движение пушки-танка влево
        """
        if self.x >= 50:
            self.x -= self.vx

    def draw(self):
        """
        Отрисовка пушки-танка
        """
        if self.live != 0:
            x = self.x
            y = self.y
            g = [(x - 20, y + 10), (x + 20, y + 10), (x + 20, y), (x - 20, y)]
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
            pygame.draw.polygon(self.screen, self.color, g)

    def test(self, obj):
        """
        Проверка на попадание сторонних "пуль" в пушку, её уничтожение
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r * 3 + obj.r) ** 2:
            self.live = 0
            return True
        return False

    def gungun(self, event_1):
        """
        Выстрел мячом. прицеливание
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        gun = Ball(self.screen)
        self.an = math.atan2((event_1.pos[1] - self.y), (event_1.pos[0] - self.x))
        gun.vx = int(20 * math.cos(self.an))
        gun.vy = int(20 * math.sin(self.an))
        gun.x = self.x
        gun.y = self.y
        balls.append(gun)


class Target:
    def __init__(self, screen):
        """
        Конструктор класса Target
        """
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 300)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.live = 1
        self.r = randint(30, 50)
        self.color = choice(GAME_COLORS)
        self.gun = 1000
        self.screen = screen

    def move(self):
        """
        описывает движение мишени
        """
        self.x += self.vx
        self.y += self.vy
        if self.x+self.r+self.vx > 801:
            self.vx *= -1
        if self.x-self.r+self.vx < 0:
            self.vx *= -1
        if self.y+self.r+self.vy > 601:
            self.vy *= -1
        if self.y-self.r+self.vy < 0:
            self.vy *= -1

    def test(self, obj):
        """
        Проверка на уничтожение мишени
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            self.live = 0
            return True
        return False

    def draw(self):
        """
        Отрисовка мишени
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class BombTarget(Target):
    def __init__(self, screen):
        """
        Конструктор класса BombTarget, наследника Target
        """
        super().__init__(screen)
        self.x = randint(100, WIDTH - 100)
        self.y = randint(100, HEIGHT - 300)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.live = 1
        self.r = randint(30, 50)
        self.color = choice(GAME_COLORS)
        self.gun = 1000
        self.screen = screen
        self.object = randint(0, 1)

    def move(self):
        """
        Описывает движение бомбардирующей мишени
        """
        global gunballs
        self.x += self.vx
        self.y += self.vy
        self.gun -= 5
        if self.x + self.vx >= WIDTH - 50:
            self.vx *= -1
        if self.x + self.vx <= 50:
            self.vx *= -1
        if self.y + self.vy >= HEIGHT - 50:
            self.vy *= -1
        if self.y + self.vy <= 50:
            self.vy *= -1
        if self.gun % 100 == 0:
            gg = Ball(self.screen)
            gg.x = self.x
            gg.y = self.y
            gg.color = (0, 200, 0)
            gg.vx = randint(-4, 4)
            gg.vy = randint(5, 10)
            gunballs.append(gg)

    def draw(self):
        """
        Отрисовка бомбардирующей, меняющей форму, мишени
        """
        if self.object:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        else:
            x = self.x
            y = self.y
            r = self.r
            a = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
            pygame.draw.polygon(self.screen, self.color, a)


display = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
gunballs = []
count = 0
clock = pygame.time.Clock()
gun = Gun(display)
target = Target(display)
btarget = BombTarget(display)
finished = False

while not finished:
    display.fill(WHITE)
    target.draw()
    btarget.draw()
    gun.draw()
    for ball in balls:
        ball.move()
        if ball.live == 0:
            balls.remove(ball)
    btarget.move()
    target.move()
    for gunball in gunballs:
        if gunball.live >= 1:
            gunball.draw()
    for ball in balls:
        if ball.live >= 1:
            ball.draw()

    clock.tick(FPS)
    bullets_counter = f1.render('Количество пуль: ' + str(bullet), True, (180, 0, 0))
    points_counter = f1.render('Количество очков: ' + str(count), True, (180, 0, 0))
    points_counter_size = f1.size('Количество очков: ' + str(count))
    display.blit(bullets_counter, (10, 50))
    display.blit(points_counter, (WIDTH - points_counter_size[0] - 20, 50))
    if gun.live == 0:
        display.blit(f1.render('Потрачено...', True, (180, 0, 0)), (WIDTH/2-100, HEIGHT/2))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(balls) < 6:
                gun.gungun(event)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gun.move_left()
    if keys[pygame.K_RIGHT]:
        gun.move_right()

    for gunball in gunballs:
        gunball.move()
        for ball in balls:
            gunball.hittest(ball)
            ball.hittest(gunball)
            if btarget.test(ball):
                btarget = BombTarget(display)
                count += 2
            if target.test(ball):
                target = Target(display)
                count += 1
        gun.test(gunball)

pygame.quit()
