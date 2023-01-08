import random

import pygame

pygame.init()
display_width = 900
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Ну допустим, недодинозаврик")

x = 80
y = display_height / 2 + 140
width = 40
height = 80
JumpCount = 30
MakeJump = False

font = pygame.font.Font(None, 40)
score = 0
above_cactus = False


class Cactus:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self):
        if self.x >= -self.width:
            pygame.draw.rect(display, (0, 255, 0), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 50 + random.randrange(-80, 60)
            return False

    def return_self(self, radius):
        self.x = radius


class Button:
    def __init__(self, width, height, inactive_sprite, active_sprite, action=False):
        self.width = width
        self.height = height
        self.inactive_sprite = inactive_sprite
        self.active_sprite = active_sprite
        self.action = action

    def draw(self, x, y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                display.blit(self.active_sprite, (x, y))

                if click[0] == 1:
                    if self.action is not None:
                        self.action = True

                    pygame.time.delay(300)

            else:
                display.blit(self.inactive_sprite, (x, y))
                self.action = False

        else:
            display.blit(self.inactive_sprite, (x, y))
            self.action = False


Cactus_width = 20
CactusHeight = 90
CatusX = display_width - 30
CactusY = display_height / 2 + 140

clock = pygame.time.Clock()


def Main():
    global MakeJump, score
    CactusArr = []
    score = 0

    working = True
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if ceck_collision(CactusArr):
            working = False
            game_over()
            break

        mouse_click = pygame.mouse.get_pressed()
        scoreText = font.render("твои балы за ОГЭ " + str(score), 1, (0, 0, 0))

        count_scores(CactusArr)

        if mouse_click[0]:
            MakeJump = True

        display.fill((255, 255, 255))
        pygame.draw.rect(display, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(display, (0, 255, 0), (0, display_height - 80, display_width, 80))
        draw_cactus(CactusArr)
        display.blit(scoreText, (0, 0))
        pygame.display.update()
        clock.tick(80)




def draw_cactus(array):
    for cactus in array:
        check = cactus.draw()



def ceck_collision(barriers):
    global x, width

    for barrier in barriers:
        if y + height >= barrier.y:
            if barrier.x <= x <= barrier.x + barrier.width:
                return True
            elif barrier.x <= x + width <= barrier.x + barrier.width:
                return True

    return False


def count_scores(barriers):
    global score, above_cactus

    if not above_cactus:
        for barrier in barriers:
            if barrier.x <= x + width / 2 <= barrier.x + barrier.width:
                if y + height - 5 <= barrier.y:
                    above_cactus = True
                    break
    else:
        if JumpCount == -28:
            score += 1
            above_cactus = False


def game_over():
    working = True
    restart_button = Button(100, 50, pygame.image.load("data/restart-button-inactive.png"),
                            pygame.image.load("data/restart-button-active.png"))
    menu_button = Button(100, 50, pygame.image.load("data/menu-button-inactive.png"),
                         pygame.image.load("data/menu-button-active.png"))

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        info = font.render("you dead :(", 1, (0, 0, 0))
        keys = pygame.key.get_pressed()

        if restart_button.action == True:
            working = False
            Main()
            restart_button.action = False

        if menu_button.action == True:
            working = False
            Menu()

        display.fill((0, 255, 255))
        display.blit(info, (display_width / 2 - 80, 20))

        restart_button.draw(display_width / 2 - restart_button.width, display_height / 2 - restart_button.height)
        menu_button.draw(display_width / 2 - restart_button.width, display_height / 2 - restart_button.height + 40)

        pygame.display.update()
        clock.tick(60)


def Menu():
    working = True
    play_button = Button(100, 50, pygame.image.load("data/play-button-inactive.png"),
                         pygame.image.load("data/play-button-active.png"))
    menu_button = Button(100, 50, pygame.image.load("data/menu-button-inactive.png"),
                         pygame.image.load("data/menu-button-active.png"))

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        info = font.render(" ", 1, (0, 0, 0))
        keys = pygame.key.get_pressed()

        if play_button.action == True:
            working = False
            Main()

        display.fill((255, 255, 255))
        display.blit(info, (display_width / 2 - 200, 20))

        play_button.draw(display_width / 2 - play_button.width, display_height / 2 - play_button.height)

        pygame.display.update()
        clock.tick(60)


Menu()
