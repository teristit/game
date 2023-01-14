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


class Cursor(pygame.sprite.Sprite):
    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(cursor_group, all_sprites)
        self.image = cursor_image
        self.rect = self.image.get_rect()


    def position(self, mouse_pos):
        self.rect.x, self.rect.y = mouse_pos


class Start(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(button_group, all_sprites)
        self.image = button_image
        self.image = pygame.transform.scale(self.image, (280, 120))
        self.button_width = self.image.get_width()
        # self.image = pygame.transform.flip(self.image, self.button_width, 0)
        # self.image = pygame.transform.rotate(self.image, 340)
        self.rect = self.image.get_rect()
        self.button_width = self.image.get_width()
        self.button_height = self.image.get_height()
        self.rect.x = (width - self.button_width) // 2 - 35
        self.rect.y = (height - self.button_height) // 2 + 250


    # функция обработки клика
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        # проверка на нажатие кнопки
        if (self.rect.x <= x <= self.rect.x + self.button_width and
                self.rect.y <= y <= self.rect.y + self.button_height):
            game.open(screen)


class Game:
    def open(self, screen):
        # основной цикл
        while True:

            # цикл обработки событий
            for event in pygame.event.get():
                pygame.time.set_timer(MYEVENTTYPE, 1900)
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == MYEVENTTYPE:
                    SmallFish(small_fish_group)
                    OtherFish(other_fish_group)
            # получение состояния кнопок
            keys = pygame.key.get_pressed()
            player.update(player, keys)
            other_fish_group.update()
            small_fish_group.update()
            screen.blit(background, (0, 0))
            draw_count()
            other_fish_group.draw(screen)
            small_fish_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            clock.tick(60)


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


# класс других рыб
class OtherFish(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(other_fish_group, all_sprites)
        image = random.choice(list(other_fish_images.values()))
        delta = random.randrange(100, 200)
        self.image = image
        self.image = pygame.transform.scale(self.image, (delta + 10, delta))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = width
        self.rect.y = random.randrange(0, height - self.image.get_height())

    def update(self):
        self.rect.x -= 1
        global count
        for i in other_fish_group:
            if pygame.sprite.collide_mask(self, player):
                # если игрок больше, то после столкновения другая рыбка исчезает
                # счет прибавляется
                if im_w > self.image.get_width() and im.get_height() > self.image.get_height():
                    self.kill()
                    count += 1
                    change()
                # иначе исчезает игрок
                else:
                    player.kill()
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


class GameOver(pygame.sprite.Sprite):
    # функция обработки клика
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        # проверка на нажатие кнопки
        if 150 <= x <= 490 and 730 <= y <= 870:
            print(1)
        elif 890 <= x <= 1250 and 705 <= y <= 895:
            print(0)

    def open(self, screen):
        fon_image = load_image('gameover.png')
        # основной цикл
        while True:
            # цикл обработки событий
            for event in pygame.event.get():
                screen.blit(fon_image, (0, 0))
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    game_over.get_click(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:
                    pygame.mouse.set_visible(False)
                    pygame.mouse.get_focused()
                    cursor_group.draw(screen)
                    cursor.position(event.pos)
            pygame.display.flip()
            clock.tick(60)


def terminate():
    pygame.quit()
    sys.exit()

pygame.init()
# параментры окна
width = 1400
height = 950
size = width, height
# группы спрайтов
all_sprites = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
other_fish_group = pygame.sprite.Group()
small_fish_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
# загруска изображений
player_image = load_image('blue_fish.png')
food_image = load_image('small_fish.png')
background = load_image('sea.jpg')
other_fish_images = {
    'gold_fish': load_image('gold_fish.png'),
    'whale': load_image('whale.png'),
    'small_fish': load_image('small_fish2.png'),
    'turtle': load_image('turtle.png')
    }
fon_image = load_image('fon.png')
button_image = load_image('start.webp')
cursor_image = load_image("arrow.png")
im = player_image
im_w = player_image.get_width()
im_mask = pygame.mask.from_surface(im)
clock = pygame.time.Clock()
# переменная счетчик
count = 0
# переменые классов
# объявление своего события
MYEVENTTYPE = pygame.USEREVENT + 1


def run():
    global game, screen, player
    screen = pygame.display.set_mode(size)
    other_fish = OtherFish()
    player = Player()
    small_fish = SmallFish()
    start = Start()
    cursor = Cursor()
    game = Game()
    game_over = GameOver()
    # основной цикл
    while True:
        # цикл обработки событий
        for event in pygame.event.get():
            screen.blit(fon_image, (0, 0))
            button_group.draw(screen)
            button_group.update()
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                start.get_click(mouse_pos)
            elif event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(False)
                pygame.mouse.get_focused()
                cursor_group.draw(screen)
                cursor.position(event.pos)
        im = pygame.transform.scale(player_image, (im_w, im_w))
        im_mask = pygame.mask.from_surface(im)
        pygame.display.flip()
        clock.tick(60)
