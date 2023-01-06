import os
import sys

import pygame


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    return level_map


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos = tile_width * pos_x, tile_height * pos_y
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])

    def update(self, d):
        self.pos = self.pos[0] + d, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = tile_width * pos_x + 15, tile_height * pos_y + 5
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 10)

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
                field.append(Tile('empty', x, y))
            elif level[y][x] == '#':
                field.append(Tile('wall', x, y))
            elif level[y][x] == '@':
                field.append(Tile('wall', x, y))
    # вернем игрока, а также размер поля в клетках
    new_player = Player(10, 5)
    return new_player, field, x, y


def move(player, vector, takeoff=0):
    x, y = player.pos
    x, y = x, y
    flagh = False
    if vector == 'LEFT' and level[(y + 39) // tile_width][((x + delta + 15) // tile_width)] == '.':
        flagh = True
        for i in field:
            i.update(-1)
    elif vector == 'RIGHT' and level[(y + 39) // tile_width][((x + delta) // tile_width)] == '.':
        flagh = True
        for i in field:
            i.update(1)
    elif vector == 'UP' and level[(y - 2) // tile_width][((x + delta) // tile_width)] == '.':
        player.update(x, int(y - takeoff))
    elif vector == 'DOWN':
        flag = True
        while flag:
            flag = move(player, 'GRAVITY')
    elif vector == 'GRAVITY':
        if level[(y - 10) // tile_width + 1][((x + delta) // tile_width)] == '.':
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
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
level = load_level('level_1.txt')
player, field, level_x, level_y = generate_level(level)
delta = 0


def run():
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 150
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
                    move(player, 'DOWN')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            delta -= 1
            if not move(player, 'RIGHT'):
                delta += 1
        if keys[pygame.K_RIGHT]:
            delta += 1
            if not move(player, 'LEFT'):
                delta -= 1
        if takeoff > 0:
            takeoff -= gravity
        move(player, 'UP', takeoff)
        screen.fill((255, 255, 255))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
