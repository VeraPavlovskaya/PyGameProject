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


events = []
rects = []

'''for event in events:
    if event.type == pygame.MOUSEBUTTONDOWN:
        n = 1
        for rect in rects:
            if rect.collidepoint(event.pos):
                print(f'Clicked on {event}')
            n += 1'''

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
        # color = [255, 30, 200]
        pygame.display.set_caption('Main Window')
        # screen — холст, на котором нужно рисовать:
        screen = pygame.display.set_mode(size)

        pygame.draw.rect(screen, pygame.Color('red'), [29, 29, 85, 85], 3)
        # pygame.draw.rect(screen, color, [1, 1, width - 2, height - 2])
        fon = pygame.transform.scale(load_image('bg2.jpg'), (650, 480))
        store = pygame.transform.scale(load_image('store.png'), (80, 80))
        profie = pygame.transform.scale(load_image('profile2.png'), (80, 80))
        coin = pygame.transform.scale(load_image('coins.png'), (50, 50))
        dragon_collaction = pygame.transform.scale(load_image('dragon_collaction.png'), (80, 80))
        choose_level = pygame.transform.scale(load_image('select_level.crdownload'), (180, 60))
        instructions = pygame.transform.scale(load_image('instructions.jfif'), (50, 50))

        font1 = pygame.font.SysFont('freesanbold.ttf', 30)
        text1 = font1.render('My Profile', True, (0, 0, 0))
        text2 = font1.render('Dragon rings:', True, (0, 0, 0))

        screen.blit(fon, (0, 0))
        #
        AREA_WIDTH = 440
        AREA_HEIGHT = 330
        AREA_LEFT = 120
        AREA_TOP = 70
        area_size = (AREA_WIDTH, AREA_HEIGHT)
        #

        profile_area = pygame.Surface(area_size)
        store_area = pygame.Surface(area_size)
        instructions_area = pygame.Surface(area_size)
        dragon_collaction_area = pygame.Surface(area_size)
        #

        rect = pygame.Rect(0, 0, AREA_WIDTH, AREA_HEIGHT)
        pygame.draw.rect(store_area, pygame.Color('lightblue'), rect)
        pygame.draw.rect(profile_area, pygame.Color('orange'), rect)
        pygame.draw.rect(dragon_collaction_area, pygame.Color('orange'), rect)
        pygame.draw.rect(instructions_area, pygame.Color('white'), rect)

        store_x = 30
        store_y = 250
        profile_x = 30
        profile_y = 70
        instructions_x = 570
        instructions_y = 50
        d_c_x = 30
        d_c_y = 200

        screen.blit(store, (store_x, store_y))
        screen.blit(profie, (profile_x, profile_y))
        screen.blit(instructions, (instructions_x, instructions_y))
        screen.blit(dragon_collaction, (d_c_x, d_c_y))
        #

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (70, 160)
        textRect2.center = (250, 50)
        #
        fps = 60
        clock = pygame.time.Clock()
        run = True
        while run:

            screen.blit(coin, (330, 20))
            screen.blit(choose_level, (250, 400))
            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)
            #
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("pygame.MOUSEBUTTONDOWN")
                    x, y = event.pos
                    print(store.get_rect())
                    print(x-store_x, y-store_y)
                    if store.get_rect().collidepoint(x - store_x, y - store_y) \
                            or dragon_collaction.get_rect().collidepoint(x - d_c_x, y - d_c_y):
                        screen.blit(store_area, (AREA_LEFT, AREA_TOP))
                    if profie.get_rect().collidepoint(x - profile_x, y - profile_y):
                        screen.blit(profile_area, (AREA_LEFT, AREA_TOP))
                    if instructions.get_rect().collidepoint(x - instructions_x, y - instructions_y):
                        screen.blit(instructions_area, (AREA_LEFT, AREA_TOP))
                        text_font = pygame.font.SysFont("Arial", 16)
                        black = (0, 0, 0)
                        with open('instructions.txt', 'r', encoding='utf-8') as using_file:
                            lines = using_file.readlines()
                        text = text_font.render((lines[2].replace('/n', '')), True, black)
                        print(lines[2])
                        screen.blit(text, (AREA_LEFT, AREA_TOP))

            #
            clock.tick(fps)
            pygame.display.flip()
            pygame.display.update()
            if event.type == pygame.QUIT:
                run = False
        # завершение работы:
        pygame.quit()
