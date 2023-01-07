import os
import sys
from random import choice

import pygame


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    return level_map


def load_image(name, type=0):
    fullname = os.path.join('data\platformerimage', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if type:
        image = pygame.transform.scale(image, (tile_width, tile_height))
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos = tile_width * pos_x, tile_height * pos_y
        self.tile_type = tile_type
        if tile_type == 1:
            self.image = choice(tile_images)
        elif tile_type == 2:
            self.image = fire_images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])

    def update(self, d):
        if self.tile_type == 2:
            self.image = fire_images[(fire_images.index(self.image) + 1) % len(fire_images)]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = self.pos[0] + d, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = tile_width * pos_x + 15, tile_height * pos_y + 10
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y):
        pos_x, pos_y = x, y
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    field = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '#':
                field.append(Tile(1, x, y))
            elif level[y][x] == '@':
                field.append(Tile(2, x, y))
    # вернем игрока, а также размер поля в клетках
    new_player = Player(10, 5)
    return new_player, field, x, y


def move(player, vector, takeoff=0):
    x, y = player.pos
    x, y = x, y
    flagh = False
    if vector == 'LEFT' and level[(y + 39) // tile_width][((x + delta + 10) // tile_width)] == '.':
        flagh = True
        for i in field:
            i.update(-speed)
    elif vector == 'RIGHT' and level[(y + 39) // tile_width][((x + delta + 10) // tile_width)] == '.':
        flagh = True
        for i in field:
            i.update(speed)
    elif vector == 'UP' and level[(y - 2) // tile_width][((x + delta + 10) // tile_width)] == '.':
        player.update(x, int(y - takeoff))
    elif vector == 'DOWN':
        flag = True
        while flag:
            flag = move(player, 'GRAVITY')
    elif vector == 'GRAVITY':
        if level[(y - 10) // tile_width + 1][((x + delta + 10) // tile_width)] == '.':
            player.update(x, y + 1)
            return True
        else:
            return False
    return flagh


def terminate():
    pygame.quit()
    sys.exit()


size = width, height = 1500, 800
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = 50
tile_height = 50
tiles = []
player_image = load_image('mar.png')
tile_images = [load_image('obj_stoneblock001.png', 1), load_image('obj_stoneblock002.png', 1),
               load_image('obj_stoneblock003.png', 1), load_image('obj_stoneblock004.png', 1),
               load_image('obj_stoneblock005.png', 1), load_image('obj_stoneblock006.png', 1),
               load_image('obj_stoneblock008.png', 1), load_image('obj_stoneblock009.png', 1)]
fire_images = [load_image('0001.png', 1), load_image('0002.png', 1), load_image('0003.png', 1),
               load_image('0004.png', 1), load_image('0005.png', 1), load_image('0006.png', 1),
               load_image('0007.png', 1), load_image('0008.png', 1), load_image('0009.png', 1),
               load_image('0010.png', 1), load_image('0011.png', 1), load_image('0012.png', 1),
               load_image('0013.png', 1), load_image('0014.png', 1), load_image('0015.png', 1),
               load_image('0016.png', 1), load_image('0017.png', 1), load_image('0018.png', 1),
               load_image('0019.png', 1), load_image('0020.png', 1), load_image('0021.png', 1),
               load_image('0022.png', 1), load_image('0023.png', 1), load_image('0024.png', 1),
               load_image('0025.png', 1), load_image('0026.png', 1), load_image('0027.png', 1),
               load_image('0028.png', 1), load_image('0029.png', 1), load_image('0030.png', 1),
               load_image('0031.png', 1), load_image('0032.png', 1), load_image('0033.png', 1),
               load_image('0034.png', 1), load_image('0035.png', 1), load_image('0036.png', 1),
               load_image('0037.png', 1), load_image('0038.png', 1), load_image('0039.png', 1),
               load_image('0040.png', 1), load_image('0041.png', 1), load_image('0042.png', 1),
               load_image('0043.png', 1), load_image('0044.png', 1), load_image('0045.png', 1),
               load_image('0046.png', 1), load_image('0047.png', 1), load_image('0048.png', 1),
               load_image('0049.png', 1), load_image('0050.png', 1)]
level = load_level('level_1.txt')
player, field, level_x, level_y = generate_level(level)
delta = 0
speed = 2


def run():
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 150
    background_image = load_image('background.jpg')
    background_image = pygame.transform.scale(background_image, (width * 5, height))
    music = pygame.mixer_music.load(os.path.join("music", "bossfight-Vextron.mp3"))
    #    pygame.mixer_music.play()
    global delta
    takeoff = 0
    gravity = 0.09

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not move(player, 'GRAVITY'):
                        takeoff = 5
                    #                        move(player, 'UP')

                    move(player, 'UP', 1)
                if event.key == pygame.K_DOWN:
                    takeoff = 0
                    move(player, 'DOWN')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            delta -= speed
            if not move(player, 'RIGHT'):
                delta += speed
        if keys[pygame.K_RIGHT]:
            delta += speed
            if not move(player, 'LEFT'):
                delta -= speed
        if takeoff > 0:
            takeoff -= gravity
        move(player, 'UP', takeoff)
        screen.fill((255, 255, 255))
        screen.blit(background_image, (-(width * 5 + delta) // 2, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
