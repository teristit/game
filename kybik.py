import pygame

pygame.init()
width = 900
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('КУУУУУУУУБИК')

x = 80
y = height / 2 + 140
wwidth = 40
hheight = 80
count = 30
running = False

font = pygame.font.Font("")
score = 0
cactus = False


class Cacih:
    def __init__(self, x, y, wwidth, hheight, speed):
        self.x = x
        self.y = y
        self.wwidth = wwidth
        self.hheight = hheight
        self.speed = speed

    def draw(self):
        if self.x >= -self.wwidth:
            pygame.draw.rect(display, (0, 250, 0), (self.x, self.y, self.wwidth, self.hheight))
            self.x -= self.speed
            return True

        else:
            self.x = display_width + 50 + random.randrange(-80, 60)
            return False