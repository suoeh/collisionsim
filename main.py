import math
import pygame
import sys
import time

pygame.init()

width, height = 1280, 720
colourH = (243, 243, 240)
colourHM = (134, 151, 150)
colourM = (118, 131, 133)
colourL = (45, 42, 46)
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load('image.png')
pygame.display.set_icon(icon)
font = pygame.font.Font("Sofia Pro Semi Bold Az.otf", 40)
pygame.display.set_caption("COLLISION SIMULATOR")


class Button:
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def draw(self):
        if self.isOver(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, colourHM, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(screen, colourM, (self.x, self.y, self.w, self.h))

        if self.text != '':
            text = font.render(self.text, 1, colourH)
            screen.blit(text,
                        (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.w:
            if self.y < pos[1] < self.y + self.h:
                return True
        return False


class Block:
    def __init__(self, mass, velocity, position, length):
        self.mass = float(mass)
        self.velocity = float(velocity)
        self.position = float(position)
        self.length = float(length)

    def checkCollision(self, other):
        if self.position + self.length >= other.position or other.position + other.length <= self.position:
            return True
        return False

    def wallCollision(self):
        if self.position + self.length >= width:
            self.velocity *= -1
            return True
        return False

    def updateMass(self, value):
        self.mass = value

    def updateVelocity(self, other):
        tempVelocity = self.velocity * ((self.mass - other.mass) / (self.mass + other.mass))
        tempVelocity += other.velocity * ((2 * other.mass) / (self.mass + other.mass))
        return round(tempVelocity, 9)

    def updatePos(self):
        self.position += self.velocity

    def draw1(self, other):
        if self.position + self.length >= width - other.length:
            pygame.draw.rect(screen, colourH,
                             (width - self.length - other.length, height // 2 - self.length, self.length, self.length))
        else:
            pygame.draw.rect(screen, colourH,
                             (self.position, height // 2 - self.length, self.length, self.length))

    def draw2(self):
        if self.position + self.length >= width:
            pygame.draw.rect(screen, colourH,
                             (width - self.length, height // 2 - self.length, self.length, self.length))
        else:
            pygame.draw.rect(screen, colourH,
                             (self.position, height // 2 - self.length, self.length, self.length))


def massToValue(mass):
    value = math.log(mass, 10)
    return (value / 8) * 350 + 400


def valueToMass(slider):
    value = 8 * (slider - 400) / 350
    return math.pow(10, value)


def simulate(mass):
    block1 = Block(mass, 0.0004, width // 6, 100)
    block2 = Block(1, 0, width // 6 + 300, 100)
    counter = 0
    start = 0
    end = False
    text = font.render("0", True, colourH)
    text_rect = text.get_rect()
    text_rect.center = (50, 50)
    text2 = font.render("0", True, colourH)
    text2_rect = text2.get_rect()
    text2_rect.center = (800, 510)
    text22 = font.render("0", True, colourH)
    text22_rect = text22.get_rect()
    text22_rect.center = (800, 560)
    text222 = font.render("0", True, colourH)
    text222_rect = text222.get_rect()
    text222_rect.center = (800, 610)
    text3 = font.render("0", True, colourH)
    text3_rect = text3.get_rect()
    text3_rect.center = (420, 510)
    text33 = font.render("0", True, colourH)
    text33_rect = text33.get_rect()
    text33_rect.center = (420, 560)
    text333 = font.render("0", True, colourH)
    text333_rect = text333.get_rect()
    text333_rect.center = (420, 610)
    points = [(0.0004, 0)]
    a = massToValue(mass)

    def update():
        text = font.render("Total collisions: " + str(counter), True, colourH)
        text2 = font.render("Right block:", True, colourH)
        text22 = font.render("Velocity: " + str(round(block2.velocity, 5)), True, colourH)
        text222 = font.render("Mass: " + str(round(block2.massw)), True, colourH)
        text3 = font.render("Left block:", True, colourH)
        text33 = font.render("Velocity: " + str(round(block1.velocity, 5)), True, colourH)
        text333 = font.render("Mass: " + str(round(block1.mass)), True, colourH)
        screen.fill(colourL)
        pygame.draw.rect(screen, colourM, (0, height // 2 - 1, width, height // 2 + 1))
        pygame.draw.rect(screen, colourHM, (0, height // 2 - 1, 185 * 2, height // 2 + 1))
        pygame.draw.rect(screen, colourL, (185, height // 2 - 1, 2, height // 2 + 1))
        pygame.draw.rect(screen, colourL, (0, 540, 185 * 2, 2))

        block1.draw1(block2)
        block2.draw2()
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text22, text22_rect)
        screen.blit(text222, text222_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text33, text33_rect)
        screen.blit(text333, text333_rect)
        pygame.draw.rect(screen, colourHM, (420, 410, 390, 40))
        pygame.draw.rect(screen, colourH, (a, 390, 80, 80))

        for x, y in points:
            xo = 150000 * x
            yo = 150000 * y * math.sqrt(block2.mass) / math.sqrt(block1.mass)
            pygame.draw.circle(screen, colourH, (185 + xo, 540 + yo), 2)
        pygame.display.update()

    while 1:
        # loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # slider
        if pygame.mouse.get_pressed()[2] != 0:
            pos = pygame.mouse.get_pos()
            a = pos[0] - 40
            if a < 400: a = 400
            if a > 750: a = 750
            block1.updateMass(valueToMass(a))

        for i in range(1000):
            if block1.checkCollision(block2):
                v_1f = block1.updateVelocity(block2)
                v_2f = block2.updateVelocity(block1)
                block1.velocity = v_1f
                block2.velocity = v_2f
                counter += 1
                if len(points) < 3142: points.append((block1.velocity, block2.velocity))

            if block2.wallCollision():
                if len(points) < 3142: points.append((block1.velocity, block2.velocity))
                counter += 1

            if block1.velocity <= block2.velocity <= 0:
                if not end:
                    end = True
                    start = time.time()
                if (time.time() - start) >= 3:
                    return

            block1.updatePos()
            block2.updatePos()

        update()


def menu():
    text = font.render("COLLISION SIMULATOR", True, colourH)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, height / 2 - 50)

    button = Button(width / 2 - 150, 350, 300, 100, 'start :D')

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button.isOver(pos):
                    option()

        screen.fill((45, 42, 46))
        button.draw()
        screen.blit(text, text_rect)
        pygame.display.update()


def option():
    text = font.render("choose mass: ", True, colourH)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, height / 2 - 50)
    button = Button(width / 2 - 150, 350, 300, 100, 'start :D')
    mass = "100"

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button.isOver(pos) and len(mass) > 0 and 0 < int(mass) <= 100000000:
                    simulate(int(mass))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(mass) > 0:
                        mass = mass[:-1]
                if pygame.K_0 <= event.key <= pygame.K_9 and len(mass) < 9:
                    character = chr(event.key)
                    mass += str(character)

        text = font.render("choose mass: " + mass, True, colourH)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, height / 2 - 50)
        screen.fill((45, 42, 46))
        button.draw()
        screen.blit(text, text_rect)
        pygame.display.update()


menu()

sys.exit()
