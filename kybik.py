import random
import pygame

pygame.init()
display_width = 900
display_height = 600
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("КУУУУБИК")

# PlayerCharacher
x = 80
y = display_height / 2 + 140
width = 40
height = 80
JumpCount = 30
MakeJump = False

font = pygame.font.Font(None, 40)
score = 0
above_cactus = False




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

        info = font.render("КУУУУУУБИК :)", 1, (0, 0, 0))
        keys = pygame.key.get_pressed()


        display.fill((255, 255, 255))
        display.blit(info, (display_width / 2 - 200, 20))

        play_button.draw(display_width / 2 - play_button.width, display_height / 2 - play_button.height)

        pygame.display.update()
        clock.tick(60)


Menu()
