import os
import pygame
import sys
from random import choice


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [list(line) for line in mapFile]

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
    if type == 1:
        image = pygame.transform.scale(image, (tile_width, tile_height))
    elif type == 2:
        image = pygame.transform.scale(image, (tile_width, tile_height))
        image = pygame.transform.flip(image, True, False)
    return image


class Foe(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = tile_width * pos_x + 15, tile_height * pos_y + 10
        self.player_images = player_image
        self.image = self.player_images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = 'IDLER'

    def update(self, x, y):
        pos_x, pos_y = x, y
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pos = tile_width * pos_x, tile_height * pos_y
        self.tile_type = tile_type
        if tile_type == 1:
            self.image = choice(tile_images)
        elif tile_type == 2:
            self.image = fire_images[0]
        elif tile_type == 3:
            self.image = foe_image[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])

    def update(self, d):
        self.pos = self.pos[0] + d, self.pos[1]
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])

    def animation(self):
        if self.tile_type == 2:
            self.image = fire_images[(fire_images.index(self.image) + 1) % len(fire_images)]
        self.mask = pygame.mask.from_surface(self.image)

    def delete(self):
        if self.tile_type == 2:
            self.image = santa_image[0]
            self.tile_type = 3


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = tile_width * pos_x + 15, tile_height * pos_y + 10
        self.player_images = player_image
        self.image = self.player_images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = 'IDLER'

    def update(self, x, y):
        pos_x, pos_y = x, y
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def animation(self, tile_type=None):
        if tile_type == 'IDLE' and self.tile_type == 'RIGHT':
            self.tile_type = 'IDLER'
        elif tile_type == 'IDLE' and self.tile_type == 'LEFT':
            self.tile_type = 'IDLEL'
        elif tile_type == 'IDLE' and self.tile_type == 'IDLER':
            self.tile_type = 'IDLER'
        elif tile_type == 'IDLE' and self.tile_type == 'IDLEL':
            self.tile_type = 'IDLEL'
        elif tile_type:
            self.tile_type = tile_type
        index = self.player_images.index(self.image)

        if self.tile_type == 'LEFT':
            self.player_images = player_walk_left
        elif self.tile_type == 'RIGHT':
            self.player_images = player_walk_right
        elif tile_type == 'UP':
            pass
        elif tile_type == 'DOWN':
            pass
        elif self.tile_type == 'IDLER':
            self.player_images = player_idle_right
        elif self.tile_type == 'IDLEL':
            self.player_images = player_idle_left
        self.image = self.player_images[(index + 1) % len(self.player_images)]
        self.mask = pygame.mask.from_surface(self.image)


def generate_level(level):
    new_player, x, y = None, None, None
    field = []
    for y in range(len(level)):
        fiel = []
        for x in range(len(level[y])):
            if level[y][x] == '.':
                fiel.append(None)
            elif level[y][x] == '#':
                fiel.append(Tile(1, x, y))
            elif level[y][x] == '@':
                fiel.append(Tile(2, x, y))
            elif level[y][x] == '(':
                fiel.append(Tile(3, x, y))
        field.append(fiel)
    # вернем игрока, а также размер поля в клетках
    new_player = Player(10, 5)
    return new_player, field, x, y


def move(player, vector, takeoff=0):
    global crutchscore
    global field
    x, y = player.pos
    x, y = x, y
    flagh = False
    if vector == 'LEFT' and level[(y + 39) // tile_width][((x + delta + 30) // tile_width)] == '.':

        flagh = True
        for i in field:
            for j in i:
                if j:
                    j.update(-speed)
    elif vector == 'RIGHT' and level[(y + 39) // tile_width][((x + delta + 10) // tile_width)] == '.':
        flagh = True
        for i in field:
            for j in i:
                if j:
                    j.update(speed)
    elif vector == 'UP' and level[(y - 2) // tile_width][((x + delta + 15) // tile_width)] == '.':
        player.update(x, int(y - takeoff))
    elif vector == 'DOWN':
        flag = True
        while flag:
            flag = move(player, 'GRAVITY')
    elif vector == 'GRAVITY':
        if level[(y - 10) // tile_width + 1][((x + delta + 10) // tile_width)] == '.':
            player.update(x, y + 1)
            return True
        elif level[(y - 10) // tile_width + 1][((x + delta + 15) // tile_width)] == '@':
            level[(y - 10) // tile_width + 1][((x + delta + 15) // tile_width)] = '.'
            field[(y - 10) // tile_width + 1][((x + delta + 15) // tile_width)].delete()
            player.update(x, y + 1)
            crutchscore += 1
            return True
        else:
            return False

    elif vector == 'LEFT' and level[(y + 39) // tile_width][((x + delta + 30) // tile_width)] == '@':
        level[(y + 39) // tile_width][((x + delta + 30) // tile_width)] == '.'
        field[(y + 39) // tile_width][((x + delta + 30) // tile_width)].delete()
        crutchscore += 1
        flagh = True
        for i in field:
            for j in i:
                if j:
                    j.update(-speed)
    elif vector == 'RIGHT' and level[(y + 39) // tile_width][((x + delta + 10) // tile_width)] == '@':
        level[(y + 39) // tile_width][((x + delta + 10) // tile_width)] = '.'
        field[(y + 39) // tile_width][((x + delta + 10) // tile_width)].delete()
        crutchscore += 1
        flagh = True
        for i in field:
            for j in i:
                if j:
                    j.update(speed)
    elif vector == 'UP' and level[(y - 2) // tile_width][((x + delta + 15) // tile_width)] == '@':
        level[(y - 2) // tile_width][((x + delta + 15) // tile_width)] = '.'
        field[(y - 2) // tile_width][((x + delta + 15) // tile_width)].delete()
        crutchscore += 1
        player.update(x, int(y - takeoff))
    return flagh


def terminate():
    pygame.quit()
    sys.exit()


def run(row):
    print(row)
    global foe_image
    global santa_image
    global level
    global delta
    global score
    global crutchscore
    global player
    global field
    global level_x
    global level_y
    global speed
    global tile_width
    global tile_height
    global tiles_group
    global all_sprites
    global tile_images, fire_images, player_group, player_image
    global player_idle_right, player_walk_right, player_walk_left, player_idle_left
    size = width, height = 1300, 800
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_width = 50
    tile_height = 50
    tiles = []
    foe_image = [load_image('foe\\idle.png', 1)]
    santa_image = [load_image('santa\\Head.png', 1), load_image('santa\\Head2.png', 1)]
    level = load_level(row)
    delta = 0
    speed = 5
    score = 0
    crutchscore = 0
    pygame.init()
    player_idle_left = [load_image('idle\\idle 1.png', 2), load_image('idle\\idle 2.png', 2),
                        load_image('idle\\idle 3.png', 2), load_image('idle\\idle 4.png', 2),
                        load_image('idle\\idle 5.png', 2), load_image('idle\\idle 6.png', 2),
                        load_image('idle\\idle 7.png', 2), load_image('idle\\idle 8.png', 2),
                        load_image('idle\\idle 9.png', 2), load_image('idle\\idle 10.png', 2)]

    player_idle_right = [load_image('idle\\idle 1.png', 1), load_image('idle\\idle 2.png', 1),
                         load_image('idle\\idle 3.png', 1), load_image('idle\\idle 4.png', 1),
                         load_image('idle\\idle 5.png', 1), load_image('idle\\idle 6.png', 1),
                         load_image('idle\\idle 7.png', 1), load_image('idle\\idle 8.png', 1),
                         load_image('idle\\idle 9.png', 1), load_image('idle\\idle 10.png', 1)]

    player_walk_left = [load_image('walk\\walk 2 (1).png', 2), load_image('walk\\walk 2 (2).png', 2),
                        load_image('walk\\walk 2 (3).png', 2), load_image('walk\\walk 2 (4).png', 2),
                        load_image('walk\\walk 2 (5).png', 2), load_image('walk\\walk 2 (6).png', 2),
                        load_image('walk\\walk 2 (7).png', 2), load_image('walk\\walk 2 (8).png', 2),
                        load_image('walk\\walk 2 (9).png', 2), load_image('walk\\walk 2 (10).png', 2)]

    player_walk_right = [load_image('walk\\walk 2 (1).png', 1), load_image('walk\\walk 2 (2).png', 1),
                         load_image('walk\\walk 2 (3).png', 1), load_image('walk\\walk 2 (4).png', 1),
                         load_image('walk\\walk 2 (5).png', 1), load_image('walk\\walk 2 (6).png', 1),
                         load_image('walk\\walk 2 (7).png', 1), load_image('walk\\walk 2 (8).png', 1),
                         load_image('walk\\walk 2 (9).png', 1), load_image('walk\\walk 2 (10).png', 1)]

    player_image = [load_image('player\\frame-1.png', 1), load_image('player\\frame-2.png', 1)]

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
    player, field, level_x, level_y = generate_level(level)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 100
    background_image = load_image('background.jpg')
    background_image = pygame.transform.scale(background_image, (width * 5, height))
    music = pygame.mixer_music.load(os.path.join("music", "bossfight-Vextron.mp3"))
    #    pygame.mixer_music.play()
    takeoff = 0
    gravity = 0.09
    image_update = 30
    image_update_counter = 0
    crutch = 0
    runGame = True

    while runGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not move(player, 'GRAVITY'):
                        takeoff = 4.8
                    #                        move(player, 'UP')

                    move(player, 'UP', 1)
                if event.key == pygame.K_DOWN:
                    takeoff = 0
                    move(player, 'DOWN')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            delta -= speed
            player.animation('RIGHT')
            if not move(player, 'RIGHT'):
                delta += speed
        elif keys[pygame.K_RIGHT]:
            delta += speed
            player.animation('LEFT')
            if not move(player, 'LEFT'):
                delta -= speed
        else:
            if player.tile_type != 'IDLE':
                player.animation('IDLE')
        if takeoff > 0:
            takeoff -= gravity
        for i in field:
            for j in i:
                if j:
                    j.animation()

        if score != crutchscore and crutch == 0:
            score = crutchscore
            crutch = 50
        elif score != crutchscore:
            crutchscore = score
        if crutch != 0:
            crutch -= 1
        print(score, '####')
        if image_update_counter // image_update == 1:
            image_update_counter = 0
            player.animation()
        image_update_counter += 1
        move(player, 'UP', takeoff)
        screen.fill((255, 255, 255))
        screen.blit(background_image, (-(width * 5 + delta) // 2, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
