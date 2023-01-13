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

        pygame.draw.rect(screen, pygame.Color('red'), [29, 29, 85, 85], 3)
        # pygame.draw.rect(screen, color, [1, 1, width - 2, height - 2])
        fon = pygame.transform.scale(load_image('bg2.jpg'), (650, 480))
        store = pygame.transform.scale(load_image('store.png'), (80, 80))
        profie = pygame.transform.scale(load_image('profile2.png'), (100, 90))
        coin = pygame.transform.scale(load_image('coins.png'), (50, 50))
        dragon_collaction = pygame.transform.scale(load_image('dragon_collaction.png'), (80, 80))

        font1 = pygame.font.SysFont('freesanbold.ttf', 30)
        text1 = font1.render('My Profile', True, (0, 255, 0))
        text2 = font1.render('Dragon rings:', True, (0, 0, 0))

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (80, 140)
        textRect2.center = (250, 50)

        run = True
        while run:
            screen.blit(fon, (0, 0))
            screen.blit(store, (40, 250))
            screen.blit(profie, (30, 30))
            screen.blit(coin, (330, 20))
            screen.blit(dragon_collaction, (40, 200))
            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)
            pygame.display.flip()
            pygame.display.update()
            while pygame.event.wait().type != pygame.QUIT:
                run = False
            # завершение работы:
            pygame.quit()


