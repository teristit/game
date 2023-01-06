import os
import sys
import pygame

# функция проверки файла на его наличие
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

pygame.init()
# параментры окна
width = 1000
height = 800
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
running = True
# основной цикл
while running:
    # цикл обработки событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0, 0))
    player_group.draw(screen)
    jellyfish_group.draw(screen)
    jellyfish_group.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()