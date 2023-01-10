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

# класс маленькой рыбы
class SmallFish(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(small_fish_group, all_sprites)
        self.image = food_image
        self.image = pygame.transform.scale(self.image, (15, 10))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = width
        self.rect.y = random.randrange(0, height - self.image.get_height())

    def update(self):
        global count
        self.rect.x -= 1
        for i in small_fish_group:
            # после столкновения маленькая рыбка исчезает
            # счет прибавляется
            if pygame.sprite.collide_mask(self, player):
                self.kill()
                count += 1
                change()
            break

# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(player_group, all_sprites)
        self.pos = width // 2, height // 2
        self.image = im
        self.mask = im_mask
        self.rect = self.image.get_rect().move(self.pos)

    def grow(self):
        global im_w
        im_w = im.get_width() + 20

    def move(self, x_pos, y_pos):
        self.pos = x_pos, y_pos
        self.rect = self.image.get_rect().move(x_pos, y_pos)

    def update(self, player, keys):
        x, y = player.pos
        if keys[pygame.K_LEFT]:
            self.image = im
            # проверка на выход за левые границы
            if x - 5 >= 0:
                x -= 5
            else:
                x = 0
        if keys[pygame.K_RIGHT]:
            # поворот изображения
            self.image = pygame.transform.flip(im, im.get_width(), 0)
            # проверка на выход за правые границы
            d_width = width - self.image.get_width()
            if x + 5 <= d_width:
                x += 5
            else:
                x = d_width
        if keys[pygame.K_DOWN]:
            self.image = pygame.transform.scale(self.image, (im_w, im_w))
            self.mask = pygame.mask.from_surface(im)
            # проверка на выход за нижние границы
            d_height = height - self.image.get_height()
            if y + 5 <= d_height:
                y += 5
            else:
                y = d_height
        if keys[pygame.K_UP]:
            self.image = pygame.transform.scale(self.image, (im_w, im_w))
            self.mask = pygame.mask.from_surface(im)
            # проверка на выход за верхние границы
            if y - 5 >= 0:
                y -= 5
            else:
                y = 0
        player.move(x, y)

# функция отрисовки счета
def draw_count():
    font = pygame.font.Font(None, 50)
    title = font.render('score:' + ' ' + str(count), True, (0, 0, 0), (66, 170, 255))
    screen.blit(title, (0, 0))

def change():
    if count == 5:
        player.grow()
    if count == 10:
        player.grow()

pygame.init()
# параментры окна
width = 1400
height = 950
size = width, height
screen = pygame.display.set_mode(size)
# группы спрайтов
all_sprites = pygame.sprite.Group()
small_fish_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# загруска изображений
player_image = load_image('blue_fish.png')
food_image = load_image('small_fish.png')
background = load_image('sea.jpg')
im = player_image
im_w = player_image.get_width()
im_mask = pygame.mask.from_surface(im)
clock = pygame.time.Clock()
# переменная счетчик
count = 0
# переменые классов
player = Player()
small_fish = SmallFish()
# объявление своего события
MYEVENTTYPE = pygame.USEREVENT + 1
running = True
# основной цикл
while running:
    # цикл обработки событий
    for event in pygame.event.get():
        pygame.time.set_timer(MYEVENTTYPE, 1900)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MYEVENTTYPE:
            SmallFish(small_fish_group)
    im = pygame.transform.scale(player_image, (im_w, im_w))
    im_mask = pygame.mask.from_surface(im)
    # получение состояния кнопок
    keys = pygame.key.get_pressed()
    player.update(player, keys)
    small_fish_group.update()
    screen.blit(background, (0, 0))
    draw_count()
    small_fish_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()