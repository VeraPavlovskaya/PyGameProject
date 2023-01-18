import os
import Dragon_Quiz
from Dragon_Quiz import GameState
import pygame
import dragonfight


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

if __name__ == '__main__':

    Dragon_Quiz.main()

    # инициализация Pygame:
    try:
        width, height = 800, 480
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
        fon = pygame.transform.scale(load_image('bg2.jpg'), (width, height))
        store = pygame.transform.scale(load_image('store.png'), (80, 80))
        profie = pygame.transform.scale(load_image('profile2.png'), (80, 80))
        coin = pygame.transform.scale(load_image('coins.png'), (50, 50))
        dragon_collaction = pygame.transform.scale(load_image('dragon_collaction.png'), (80, 80))
        choose_level = pygame.transform.scale(load_image('select_level.crdownload'), (180, 60))
        instructions = pygame.transform.scale(load_image('instructions.jfif'), (50, 50))
        play_btn = pygame.transform.scale(load_image('PlayBtn.png'), (200, 80))
        quit_btn = pygame.transform.scale(load_image('QuitBtn.png'), (200, 80))
        winter_level = pygame.transform.scale(load_image('winter_level.png'), (80, 80))
        summer_level = pygame.transform.scale(load_image('summer_level.jpg'), (80, 80))
        sea_level = pygame.transform.scale(load_image('Sea_level.png'), (80, 80))
        ### my_dragon_pic = pygame.transform.scale(load_image(filename), (50, 50))

        font1 = pygame.font.SysFont('freesanbold.ttf', 30)
        text1 = font1.render('My Profile', True, (0, 0, 0))
        text2 = font1.render('Dragon rings:', True, (0, 0, 0))

        screen.blit(fon, (0, 0))
        #
        AREA_WIDTH = 470
        AREA_HEIGHT = 300
        AREA_LEFT = 170
        AREA_TOP = 85
        IMG_WIDTH = IMG_HEIGHT = 60
        area_size = (AREA_WIDTH, AREA_HEIGHT)
        #

        profile_area = pygame.Surface(area_size)
        store_area = pygame.Surface(area_size)
        instructions_area = pygame.Surface(area_size)
        dragon_collaction_area = pygame.Surface(area_size)
        choose_level_area = pygame.Surface(area_size)

        #

        rect = pygame.Rect(0, 0, AREA_WIDTH, AREA_HEIGHT)
        pygame.draw.rect(store_area, pygame.Color('lightblue'), rect)
        pygame.draw.rect(profile_area, pygame.Color('lightblue'), rect)
        pygame.draw.rect(dragon_collaction_area, pygame.Color('lightblue'), rect)
        pygame.draw.rect(choose_level_area, pygame.Color('lightblue'), rect)
        pygame.draw.rect(instructions_area, pygame.Color('white'), rect)

        store_x = 30
        store_y = 250
        profile_x = 30
        profile_y = 70
        instructions_x = 700
        instructions_y = 50
        play_btn_x = 565
        play_btn_y = 400
        quit_btn_x = 70
        quit_btn_y = 400
        d_c_x = 30
        d_c_y = 200
        choose_level_x = 330
        choose_level_y = 395
        winter_x = 40
        winter_y = 30

        screen.blit(store, (store_x, store_y))
        screen.blit(profie, (profile_x, profile_y))
        screen.blit(instructions, (instructions_x, instructions_y))
        screen.blit(dragon_collaction, (d_c_x, d_c_y))
        screen.blit(choose_level, (choose_level_x, choose_level_y))
        screen.blit(quit_btn, (quit_btn_x, quit_btn_y))
        #

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (70, 160)
        textRect2.center = (390, 50)
        #
        fps = 60
        clock = pygame.time.Clock()
        run = True
        while run:
            #
            screen.blit(coin, (width//2 + 60, 20))
            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)
            screen.blit(play_btn, (play_btn_x, play_btn_y))
            #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print("pygame.MOUSEBUTTONDOWN")
                    x, y = event.pos
                    # print(store.get_rect())
                    # print(x-store_x, y-store_y)
                    text_font = pygame.font.SysFont("Arial", 16)
                    if store.get_rect().collidepoint(x - store_x, y - store_y) \
                            or dragon_collaction.get_rect().collidepoint(x - d_c_x, y - d_c_y):
                        # Print title on store area
                        title = font1.render('My Dragons:', True, (230, 0, 0))
                        title_height = title.get_rect().height
                        store_area.blit(title, (width // 2 - AREA_WIDTH // 2, 5))
                        # Print dragon image on store area
                        for i in range(len(Dragon_Quiz.my_dragon_list)):
                            file_name = Dragon_Quiz.my_dragon_list[i]
                            img = pygame.transform.scale(load_image(file_name), (IMG_WIDTH, IMG_HEIGHT))
                            store_area.blit(img, (AREA_LEFT - AREA_LEFT // 2 + i * 80, AREA_TOP - title_height))

                        # Blit store area on main screen
                        screen.blit(store_area, (AREA_LEFT, AREA_TOP))
                    if profie.get_rect().collidepoint(x - profile_x, y - profile_y):

                        file_name = Dragon_Quiz.my_dragon[GameState.DRAGON]['file']
                        img = pygame.transform.scale(load_image(file_name), (IMG_WIDTH, IMG_HEIGHT))
                        profile_area.blit(img, (10, 10))

                        title = font1.render('Player1', True, (110, 52, 1))
                        title_height = title.get_rect().height
                        profile_area.blit(title, (5, IMG_HEIGHT + 15))

                        screen.blit(profile_area, (AREA_LEFT, AREA_TOP))
                    if instructions.get_rect().collidepoint(x - instructions_x, y - instructions_y):
                        black = (0, 0, 0)
                        with open('instructions.txt', 'r', encoding='utf-8') as using_file:
                            lines = using_file.readlines()
                        i = 0
                        for line in lines:
                            text = text_font.render(line.strip(), True, black)
                            instructions_area.blit(text, (5, 5 + text.get_rect().height*i))
                            i += 1
                        screen.blit(instructions_area, (AREA_LEFT, AREA_TOP))

                    if choose_level.get_rect().collidepoint(x - choose_level_x, y - choose_level_y):
                        title = font1.render('Select level to continue', True, (110, 52, 1))
                        title_height = title.get_rect().height
                        choose_level_area.blit(title, (5, 5))
                        choose_level_area.blit(winter_level, (winter_x, winter_y))
                        choose_level_area.blit(summer_level, (winter_x + 120, winter_y))
                        choose_level_area.blit(sea_level, (winter_x + 240, 30))
                        print(choose_level_x - winter_x, choose_level_y - winter_y)

                        if winter_level.get_rect().collidepoint(AREA_WIDTH - winter_x, AREA_TOP - winter_y):
                            ###
                            print('bliting')
                        screen.blit(choose_level_area, (AREA_LEFT, AREA_TOP))
                    if play_btn.get_rect().collidepoint(x - play_btn_x, y - play_btn_y):
                        dragonfight.main(1)
                    if quit_btn.get_rect().collidepoint(x - quit_btn_x, y - quit_btn_y):
                        run = False
            #
            clock.tick(fps)
            pygame.display.flip()
            pygame.display.update()
        # завершение работы:
        pygame.quit()
