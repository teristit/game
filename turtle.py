import os
import sys
import pygame
import random

# функция проверки файла на его наличие
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# класс медуз
class Jellyfish(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(jellyfish_group, all_sprites)
        self.image = food_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randrange(5, width - 5)
        self.rect.y = height

    def update(self):
        self.rect.y -= 1
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

# класс черепахи
class Turtle(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(player_group, all_sprites)
        self.pos = width // 2, height // 2
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos)


pygame.init()
# параментры окна
width = 1400
height = 950
size = width, height
screen = pygame.display.set_mode(size)
# группы спрайтов
all_sprites = pygame.sprite.Group()
jellyfish_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# загруска изображений
player_image = load_image('turtle.png')
food_image = load_image('медуза.png')
background = load_image('sea.jpg')
clock = pygame.time.Clock()
# переменые классов
turtle = Turtle()
jellyfish = Jellyfish()
# объявление своего события
MYEVENTTYPE = pygame.USEREVENT + 1
time = random.randrange(1000, 10000)
running = True
# основной цикл
while running:
    # цикл обработки событий
    for event in pygame.event.get():
        pygame.time.set_timer(MYEVENTTYPE, time)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MYEVENTTYPE:
            time = random.randrange(1000, 10000)
            Jellyfish(jellyfish_group)
    screen.blit(background, (0, 0))
    player_group.draw(screen)
    jellyfish_group.draw(screen)
    jellyfish_group.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()