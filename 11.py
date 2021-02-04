import pygame
import random

pygame.init()

width = 800
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()
pygame.mixer.init()
go_flag = False

black = (0, 0, 0)
end_it = False
run = True
g_flag = False
bg = pygame.image.load('images/startscreen.jpg')
bg = pygame.transform.scale(bg, (800, 800))
while (end_it == False):
    for event in pygame.event.get():
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            # if event.type == pygame.K_SPACE:
            gamemode = 1
            end_it = True
        elif keys[pygame.K_m]:
            gamemode = 2
            end_it = True
        elif keys[pygame.K_h]:
            gamemode = 3
            end_it = True
        elif keys[pygame.K_g]:
            gamemode = 4
            end_it = True
        elif event.type == pygame.QUIT:
            run = False
    screen.blit(bg, (0, 0))
    pygame.display.flip()


class Ball(object):
    def __init__(self, x, y, w, h, color, gamemode):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        if gamemode < 4:
            self.xv = gamemode * 5
            self.yv = gamemode * 5
        else:
            self.xv = 9
            self.yv = 9
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])


class Platform(object):
    def __init__(self, x, y, w, h, color):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])


class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.yy = self.y + self.h

        n = random.randint(0, 100)
        if n < 5:
            self.f = True
        else:
            self.f = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h])


if gamemode == 1:
    brickcolor = (0, 200, 0)
    ballcolor = (255, 10, 10)
    player = Platform(width / 2 - 50, height - 100, 160, 20, (0, 200, 150))
    bg = pygame.image.load('images/bg1.jpg')
    bg = pygame.transform.scale(bg, (800, 800))
    lines = 3
    pygame.mixer.music.load('Soundtrack/Игорь Николаев - Выпьем за любовь.mp3')

elif gamemode == 2:
    brickcolor = (0, 0, 255)
    ballcolor = (200, 200, 200)
    player = Platform(width / 2 - 50, height - 100, 130, 20, (150, 150, 150))
    bg = pygame.image.load('images/bg3.jpg')
    bg = pygame.transform.scale(bg, (800, 800))
    lines = 5
    pygame.mixer.music.load('Soundtrack/Вставай Донбасс.mp3')

elif gamemode == 3:
    brickcolor = (255, 0, 0)
    ballcolor = (0, 0, 0)
    player = Platform(width / 2 - 50, height - 100, 70, 20, (50, 1, 1))
    bg = pygame.image.load('images/bg2.jpg')
    bg = pygame.transform.scale(bg, (800, 800))
    lines = 7
    pygame.mixer.music.load('Soundtrack/Надежда Кадышева - Я не колдунья.mp3')

elif gamemode == 4:
    brickcolor = (0, 0, 255)
    ballcolor = (255, 10, 10)
    player = Platform(width / 2 - 50, height - 100, 130, 20, (150, 230, 200))
    bg = pygame.image.load('images/billy.jpg')
    bg = pygame.transform.scale(bg, (800, 800))
    lines = 5
    pygame.mixer.music.load('Soundtrack/secretsong.mp3')

bricks = []
ball = Ball(width / 2 - 10, height - 400, 20, 20, ballcolor, gamemode)
balls = []
balls.append(ball)
bricks = []
for i in range(lines):
    for j in range(10):
        bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, brickcolor))

pygame.mixer.music.play()
run = True
while run:
    clock.tick(100)
    if not go_flag:
        for ball in balls:
            ball.x += ball.xv
            ball.y += ball.yv
        if (pygame.mouse.get_pos()[0] - player.w // 2) < 0:
            player.x = 0
        elif (pygame.mouse.get_pos()[0] + player.w // 2) > width:
            player.x = width - player.w
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w // 2

        for ball in balls:
            if (ball.x >= player.x and ball.x <= player.x + player.w) or \
                    (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                if ball.y + ball.h >= player.y and ball.y + ball.h <= player.y + player.h:
                    ball.yv *= -1
                    ball.y = player.y - ball.h - 1

            if ball.x + ball.w >= width:
                ball.xv *= -1
            if ball.x < 0:
                ball.xv *= -1
            if ball.y <= 0:
                ball.yv *= -1

            if ball.y > height:
                balls.pop(balls.index(ball))

        for brick in bricks:
            for ball in balls:
                if (ball.x >= brick.x and ball.x <= brick.x + brick.w) or \
                        ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w:
                    if (ball.y >= brick.y and ball.y <= brick.y + brick.h) or \
                            ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y + brick.h:
                        brick.visible = False
                        if brick.f:
                            balls.append(Ball(brick.x, brick.y, 20, 20, ballcolor, gamemode))
                        # bricks.pop(bricks.index(brick))
                        ball.yv *= -1
                        break

        if len(balls) == 0:
            go_flag = True

        for brick in bricks:
            if brick.visible == False:
                bricks.pop(bricks.index(brick))

    keys = pygame.key.get_pressed()
    if len(bricks) == 0:
        win_flag = True
        go_flag = True
    if go_flag:
        if keys[pygame.K_e]:
            go_flag = False
            win_flag = False
            gamemode = 1
            ball = Ball(width / 2 - 10, height - 400, 20, 20, (255, 255, 255), gamemode)
            if len(balls) == 0:
                balls.append(ball)

        elif keys[pygame.K_m]:
            go_flag = False
            win_flag = False
            gamemode = 2
            ball = Ball(width / 2 - 10, height - 400, 20, 20, (255, 255, 255), gamemode)
            if len(balls) == 0:
                balls.append(ball)

        elif keys[pygame.K_h]:
            go_flag = False
            win_flag = False
            gamemode = 3
            ball = Ball(width / 2 - 10, height - 400, 20, 20, (255, 255, 255), gamemode)
            if len(balls) == 0:
                balls.append(ball)

        elif keys[pygame.K_g]:
            go_flag = False
            win_flag = False
            gamemode = 4
            ball = Ball(width / 2 - 10, height - 400, 20, 20, (255, 255, 255), gamemode)
            if len(balls) == 0:
                balls.append(ball)

        # print(gamemode)

        if gamemode == 1:
            brickcolor = (0, 255, 0)
            ballcolor = (255, 10, 10)
            player = Platform(width / 2 - 50, height - 100, 160, 20, (0, 200, 150))
            bg = pygame.image.load('images/bg1.jpg')
            bg = pygame.transform.scale(bg, (800, 800))
            lines = 3
            pygame.mixer.music.load('Soundtrack/Игорь Николаев - Выпьем за любовь.mp3')

        elif gamemode == 2:
            brickcolor = (0, 0, 255)
            ballcolor = (255, 10, 10)
            player = Platform(width / 2 - 50, height - 100, 130, 20, (150, 150, 150))
            bg = pygame.image.load('images/bg3.jpg')
            bg = pygame.transform.scale(bg, (800, 800))
            lines = 5
            pygame.mixer.music.load('Soundtrack/Вставай Донбасс.mp3')

        elif gamemode == 3:
            brickcolor = (255, 0, 0)
            ballcolor = (0, 0, 0)
            player = Platform(width / 2 - 50, height - 100, 70, 20, (50, 1, 1))
            bg = pygame.image.load('images/bg2.jpg')
            bg = pygame.transform.scale(bg, (800, 800))
            lines = 7
            pygame.mixer.music.load('Soundtrack/Надежда Кадышева - Я не колдунья.mp3')

        elif gamemode == 4:
            brickcolor = (0, 100, 200)
            ballcolor = (255, 10, 10)
            player = Platform(width / 2 - 50, height - 100, 130, 20, (150, 150, 150))
            bg = pygame.image.load('images/billy.jpg')
            bg = pygame.transform.scale(bg, (800, 800))
            lines = 5
            pygame.mixer.music.load('Soundtrack/secretsong.mp3')

        ball = Ball(width / 2 - 10, height - 400, 20, 20, ballcolor, gamemode)
        balls = []
        if len(balls) == 0:
            balls.append(ball)

        bricks = []
        for i in range(lines):
            for j in range(10):
                bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, brickcolor))

        pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(bg, (0, 0))
    player.draw(screen)
    for b in bricks:
        b.draw(screen)
    for ball in balls:
        ball.draw(screen)

    font = pygame.font.SysFont('comicsans', 50)

    if go_flag:
        if len(bricks) == 0:
            bg = pygame.image.load('images/winscreen.jpg')
            bg = pygame.transform.scale(bg, (800, 800))
        else:
            bg = pygame.image.load('images/losescreen.jpg')
            bg = pygame.transform.scale(bg, (800, 800))

        screen.blit(bg, (0, 0))

    pygame.display.update()

pygame.quit()
