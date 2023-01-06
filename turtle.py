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
        self.rect.x = random.randrange(30, width - self.image.get_width() - 30)
        self.rect.y = height

    def update(self):
        self.rect.y -= 1
        if pygame.sprite.collide_mask(self, turtle):
            self.kill()


# класс черепахи
class Turtle(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(player_group, all_sprites)
        self.pos = width // 2, height // 2
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos)

    def move(self, x_pos, y_pos):
        self.pos = x_pos, y_pos
        self.rect = self.image.get_rect().move(x_pos, y_pos)

    def update(self, turtle, keys):
        x, y = turtle.pos
        if keys[pygame.K_LEFT]:
            # проверка на выход за левые границы
            if x - 5 >= 0:
                x -= 5
            else:
                x = 0
        elif keys[pygame.K_RIGHT]:
            d_width = width - self.image.get_width()
            # проверка на выход за правые границы
            if x + 5 <= d_width:
                x += 5
            else:
                x = d_width
        if keys[pygame.K_DOWN]:
            d_height = height - self.image.get_height()
            # проверка на выход за нижние границы
            if y + 5 <= d_height:
                y += 5
            else:
                y = d_height
        elif keys[pygame.K_UP]:
            # проверка на выход за верхние границы
            if y - 5 >= 0:
                y -= 5
            else:
                y = 0
        turtle.move(x, y)


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
time = random.randrange(1900, 10000)
running = True
# основной цикл
while running:
    # цикл обработки событий
    for event in pygame.event.get():
        pygame.time.set_timer(MYEVENTTYPE, time)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MYEVENTTYPE:
            time = random.randrange(1900, 10000)
            Jellyfish(jellyfish_group)
    # получение состояния кнопок
    keys = pygame.key.get_pressed()
    turtle.update(turtle, keys)
    screen.blit(background, (0, 0))
    player_group.draw(screen)
    jellyfish_group.draw(screen)
    jellyfish_group.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()