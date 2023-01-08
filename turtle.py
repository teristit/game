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
        global count
        self.rect.y -= 1
        for i in jellyfish_group:
            if pygame.sprite.collide_mask(self, turtle):
                count += 1
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
            self.image = player_image
            # проверка на выход за левые границы
            if x - 5 >= 0:
                x -= 5
            else:
                x = 0
        elif keys[pygame.K_RIGHT]:
            # поворот изображения
            self.image = pygame.transform.flip(player_image, player_image.get_width(), 0)
            # проверка на выход за правые границы
            d_width = width - self.image.get_width()
            if x + 5 <= d_width:
                x += 5
            else:
                x = d_width
        if keys[pygame.K_DOWN]:
            # проверка на выход за нижние границы
            d_height = height - self.image.get_height()
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

# функция отрисовки счета
def draw_count():
    font = pygame.font.Font(None, 50)
    title = font.render(str(count), True, (100, 255, 100))
    screen.blit(title, (0, 0))

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
# переменная счетчик
count = 0
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
    jellyfish_group.update()
    screen.blit(background, (0, 0))
    draw_count()
    jellyfish_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()