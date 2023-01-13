import os

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

if __name__ == '__main__':
    # инициализация Pygame:
    try:
        width, height = 650, 480
    except ValueError:
        print('Неправильный формат ввода')
        exit()
    else:
        pygame.init()
        # размеры окна:
        size = width, height  # = 800, 600
        color = [255, 30, 200]
        pygame.display.set_caption('Main Window')
        # screen — холст, на котором нужно рисовать:
        screen = pygame.display.set_mode(size)
        # pygame.draw.rect(screen, color, [1, 1, width - 2, height - 2])
        fon = pygame.transform.scale(load_image('bg2.jpg'), (650, 480))
        store = pygame.transform.scale(load_image('store.png'), (80, 80))
        profie = pygame.transform.scale(load_image('profile2.png'), (100, 90))
        font1 = pygame.font.SysFont('freesanbold.ttf', 30)
        text1 = font1.render('My Profile', True, (0, 255, 0))
        textRect1 = text1.get_rect()
        textRect1.center = (80, 150)

        run = True
        while run:
            screen.blit(fon, (0, 0))
            screen.blit(store, (30, 250))
            screen.blit(profie, (30, 50))
            screen.blit(text1, textRect1)
            pygame.display.flip()
            while pygame.event.wait().type != pygame.QUIT:
                run = False
            # завершение работы:
            pygame.quit()


