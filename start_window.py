import os
import sys
import pygame


# Начальное окно
class StartWindow:
    # функция проверки существования загружаемого файла
    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    # функция прорисовки кнопок
    def draw(self, screen):
        names = ['TITLE GAME', 'name', 'name', 'name', 'name']
        for i in range(len(names)):
            if i == 0:
                font_size = 100
            else:
                font_size = 50
            font = pygame.font.Font(None, font_size)
            title = font.render(names[i], True, (100, 255, 100))
            text_x = width // 2 - title.get_width() // 2
            text_y = 30 + 150 * i
            text_w = title.get_width()
            text_h = title.get_height()
            screen.blit(title, (text_x, text_y))
            if i != 0:
                pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 1)

    # функция обработки клика
    def get_click(self, mouse_pos):
        x, y = mouse_pos
        names = ['name', 'name', 'name', 'name']
        for i in range(1, len(names) + 1):
            font = pygame.font.Font(None, 50)
            title = font.render(names[i - 1], True, (100, 255, 100))
            button_x = (width // 2 - title.get_width() // 2) - 10
            button_y = 30 + 150 * i
            button_w = title.get_width()
            button_h = title.get_height() + 10
            # проверка на нажатие кнопки
            if (button_x <= x <= button_x + button_w and
                    button_y <= y <= button_y + button_h):
                # переход в окно игры 1
                if i == 1:
                    print(4)
                # переход в окно игры 2
                elif i == 2:
                    print(3)
                    sys.exit()
                # переход в окно игры 3
                elif i == 3:
                    print(2)
                else:
                    print(1)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Начальная заставка')
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    start_window = StartWindow()
    runGame = True
    # игровой цикл
    while runGame:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                start_window.get_click(mouse_pos)
                if runGame == False:
                    break
            background = start_window.load_image('background.jpg')
            screen.blit(background, (0, 0))
            start_window.draw(screen)
            pygame.display.flip()
    pygame.quit()