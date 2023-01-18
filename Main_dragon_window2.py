import os
import Dragon_Quiz
from Dragon_Quiz import GameState
import pygame
import dragonfight


def draw_new_coins():
    coins_text = font1.render(str(CURRENT_COINS), True, (0, 0, 0))
    coins_rect = coins_text.get_rect()
    # pygame.draw.rect(store_area, pygame.Color('lightblue'), bckgr_rect)
    coins_rect.center = (334 + coin.get_rect().width // 2, 12 + coin.get_rect().height // 2)
    screen.blit(coins_text, coins_rect)


def hide_old_coins():
    cr_x = 360
    cr_y = 34
    cr_w = 50
    cr_h = 20
    fon_color = fon.get_at((cr_x, cr_y))
    bckgr_rect = pygame.Rect(cr_x, cr_y, cr_w, cr_h)
    pygame.draw.rect(screen, fon_color, bckgr_rect)  # To Hide old coins value


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


def draw_dragon_shop():
    bckgr_rect = pygame.Rect(0, 205, AREA_WIDTH, 25)  # Hide old message
    pygame.draw.rect(store_area, pygame.Color('lightblue'), bckgr_rect)
    ln = len(Dragon_Quiz.my_dragon_list)
    for i in range(ln):
        img_file_name = Dragon_Quiz.my_dragon_list[i]["file"]
        dragon_img = pygame.transform.scale(load_image(img_file_name, -1), (IMG_WIDTH, IMG_HEIGHT))
        Dragon_Quiz.my_dragon_list[i]["image"] = dragon_img
        img_height = dragon_img.get_rect().height
        img_width = dragon_img.get_rect().width
        # images evenly distributed horizontally
        di = (AREA_WIDTH - ln*img_width) // (ln + 1)
        xi = di + (di+img_width)*i
        clr = (230, 20, 20) if Dragon_Quiz.my_dragon_list[i]["active"] == "Y" else (128, 128, 128)
        lbl_name = font2.render(Dragon_Quiz.my_dragon_list[i]["name"], True, clr)
        name_height = lbl_name.get_rect().height
        name_width = lbl_name.get_rect().width
        # Image and text centered vertically
        yi = (AREA_HEIGHT - img_height - 30 - 20)//2
        xt = xi + (img_width - name_width) // 2
        yt = yi + img_height + 20
        store_area.blit(dragon_img, (xi, yi))
        store_area.blit(lbl_name, (xt, yt))
        #
        pygame.draw.rect(store_area, (255, 255, 255), (xi, yi, img_width, img_height), 3)
        if SELECTED_DRAGON == i:
            pygame.draw.rect(store_area, (0, 0, 255), (xi, yi, img_width, img_height), 3)
        if Dragon_Quiz.my_dragon_list[i]["active"] == "N":
            grey_rect = pygame.Surface((img_width, img_height), pygame.SRCALPHA)
            grey_rect.fill((192, 192, 192, 128))
            store_area.blit(grey_rect, (xi, yi))
            #
            # Draw Price for inactive Dragons
            lbl_prc = font2.render("Price: " + str(Dragon_Quiz.my_dragon_list[i]["price"]), True, clr)
            prc_height = lbl_prc.get_rect().height
            prc_width = lbl_prc.get_rect().width
            xp = xt + (name_width - prc_width) // 2
            yp = yt + name_height + 5
            #print("yp=", yp)
            store_area.blit(lbl_prc, (xp, yp))

    screen.blit(store_area, (AREA_LEFT, AREA_TOP))


def draw_levels():
    for i in range(len(levels)):
        img_w = levels[i]["image"].get_rect().width
        img_h = levels[i]["image"].get_rect().height
        choose_level_area.blit(levels[i]["image"], (winter_x + i * 120, winter_y))
        pygame.draw.rect(choose_level_area, (255, 255, 255),
                         (winter_x + i * 120, winter_y, img_w, img_h), 3)
        if i == ACTIVE_LEVEL:
            print('Init ACTIVE_LEVEL:', i)
    pygame.draw.rect(choose_level_area, (0, 0, 255),
                     (winter_x + ACTIVE_LEVEL * 120, winter_y, img_w, img_h), 3)
    screen.blit(choose_level_area, (AREA_LEFT, AREA_TOP))


if __name__ == '__main__':

    Dragon_Quiz.main()

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
        fon = pygame.transform.scale(load_image('bg2.jpg'), (width, height))
        store = pygame.transform.scale(load_image('store.png'), (80, 80))
        profie = pygame.transform.scale(load_image('profile2.png'), (80, 80))
        coin = pygame.transform.scale(load_image('coins.png'), (100, 65))
        dragon_collaction = pygame.transform.scale(load_image('dragon_collaction.png'), (80, 80))
        choose_level = pygame.transform.scale(load_image('select_level.crdownload'), (180, 60))
        instructions = pygame.transform.scale(load_image('instructions.jfif'), (50, 50))
        play_btn = pygame.transform.scale(load_image('PlayBtn.png'), (200, 80))
        quit_btn = pygame.transform.scale(load_image('QuitBtn.png'), (200, 80))
        winter_level = pygame.transform.scale(load_image('winter_level.png'), (80, 80))
        summer_level = pygame.transform.scale(load_image('summer_level.jpg'), (80, 80))
        sea_level = pygame.transform.scale(load_image('Sea_level.png'), (80, 80))

        levels = [{"id": 0, "name": "winter", "image": winter_level},
                  {"id": 1, "name": "summer", "image": summer_level},
                  {"id": 2, "name": "sea", "image": sea_level}]
        ACTIVE_LEVEL = 0
        inLevel = False
        inStore = False
        SELECTED_DRAGON = 0
        SELECTED_DRAGON_NAME = GameState.DRAGON
        for i in range(len(Dragon_Quiz.my_dragon_list)):
            if Dragon_Quiz.my_dragon_list[i]["name"] == GameState.DRAGON:
                SELECTED_DRAGON = i
        CURRENT_COINS = 1500
        ### my_dragon_pic = pygame.transform.scale(load_image(filename), (50, 50))

        font1 = pygame.font.SysFont('freesanbold.ttf', 30)
        font2 = pygame.font.SysFont('freesanbold.ttf', 25)
        text1 = font1.render('My Profile', True, (0, 0, 0))
        text2 = font1.render('Dragon rings:', True, (0, 0, 0))

        screen.blit(fon, (0, 0))
        hide_old_coins()
        ##-----------------------------------------------------------------
        #
        AREA_WIDTH = 430
        AREA_HEIGHT = 320
        AREA_LEFT = 130
        AREA_TOP = 75
        IMG_WIDTH = IMG_HEIGHT = 60
        area_size = (AREA_WIDTH, AREA_HEIGHT)
        #

        profile_area = pygame.Surface(area_size)
        store_area = pygame.Surface(area_size)
        instructions_area = pygame.Surface(area_size)
        dragon_collaction_area = pygame.Surface(area_size)
        choose_level_area = pygame.Surface(area_size)

        #

        area_rect = pygame.Rect(0, 0, AREA_WIDTH, AREA_HEIGHT)
        pygame.draw.rect(store_area, pygame.Color('lightblue'), area_rect)
        pygame.draw.rect(profile_area, pygame.Color('lightblue'), area_rect)
        pygame.draw.rect(dragon_collaction_area, pygame.Color('lightblue'), area_rect)
        pygame.draw.rect(choose_level_area, pygame.Color('lightblue'), area_rect)
        pygame.draw.rect(instructions_area, pygame.Color('white'), area_rect)

        store_x = 30
        store_y = 250
        profile_x = 30
        profile_y = 70
        instructions_x = 570
        instructions_y = 50
        quit_btn_x = 0
        quit_btn_y = 390
        d_c_x = 30
        d_c_y = 200
        choose_level_x = 250
        choose_level_y = 400
        winter_x = 50
        winter_y = 100
        play_btn_x = 450
        play_btn_y = 390

        #

        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (70, 160)
        textRect2.center = (250, 43)
        #
        fps = 60
        clock = pygame.time.Clock()
        run = True
        while run:
            #
            # screen.blit(fon, (0, 0))
            screen.blit(store, (store_x, store_y))
            screen.blit(profie, (profile_x, profile_y))
            screen.blit(instructions, (instructions_x, instructions_y))
            screen.blit(dragon_collaction, (d_c_x, d_c_y))
            screen.blit(choose_level, (choose_level_x, choose_level_y))
            screen.blit(quit_btn, (quit_btn_x, quit_btn_y))
            screen.blit(coin, (330, 5))
            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)
            screen.blit(play_btn, (play_btn_x, play_btn_y))
            #
            coins_text = font1.render(str(CURRENT_COINS), True, (0, 0, 0))
            coins_rect = coins_text.get_rect()
            coins_rect.center = (334 + coin.get_rect().width//2, 12 + coin.get_rect().height//2)
            screen.blit(coins_text, coins_rect)
            #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    text_font = pygame.font.SysFont("Arial", 16)
                    if store.get_rect().collidepoint(x - store_x, y - store_y) \
                            or dragon_collaction.get_rect().collidepoint(x - d_c_x, y - d_c_y):
                        # Print title on store area
                        title = font1.render('My Dragons:', True, (230, 0, 0))
                        title_height = title.get_rect().height
                        title_width = title.get_rect().width
                        store_area.blit(title, ((AREA_WIDTH - title_width) // 2, 10))
                        #
                        activate_btn = pygame.transform.scale(load_image('Activate2.jpg', -1), (90, 40))
                        buy_btn = pygame.transform.scale(load_image('Buy2.jpg', -1), (90, 40))
                        x_act = AREA_WIDTH//3 - 90//2
                        y_act = AREA_HEIGHT*5//6 - 40//2
                        store_area.blit(activate_btn, (x_act, y_act))
                        x_buy = AREA_WIDTH//3*2 - 90//2
                        y_buy = AREA_HEIGHT*5//6 - 40//2
                        store_area.blit(buy_btn, (x_buy, y_buy))
                        # Print dragon image on store area
                        draw_dragon_shop()
                        inLevel = False
                        inStore = True
                    else:
                        if inStore:
                            bckgr_rect = pygame.Rect(0, 35, AREA_WIDTH, 50)  # Hide old message
                            pygame.draw.rect(store_area, pygame.Color('lightblue'), bckgr_rect)
                            ln = len(Dragon_Quiz.my_dragon_list)
                            for i in range(ln):
                                dragon_img = Dragon_Quiz.my_dragon_list[i]["image"]
                                img_h = dragon_img.get_rect().height
                                img_w = dragon_img.get_rect().width
                                # images evenly distributed horizontally
                                di = (AREA_WIDTH - ln * img_w) // (ln + 1)
                                xi = di + (di + img_w) * i
                                yi = (AREA_HEIGHT - img_h - 30 - 20) // 2
                                # Clicked on the Dragon
                                if dragon_img.get_rect().collidepoint(x - AREA_LEFT - xi, y - AREA_TOP - yi):
                                    #and Dragon_Quiz.my_dragon_list[i]["active"] == 'Y')
                                    SELECTED_DRAGON = i
                                    SELECTED_DRAGON_NAME = Dragon_Quiz.my_dragon_list[i]["name"]
                                    print("SELECTED_DRAGON:", SELECTED_DRAGON)
                                # Clicked on Activate
                            if (activate_btn.get_rect().collidepoint(x - AREA_LEFT - x_act, y - AREA_TOP - y_act)
                                   and Dragon_Quiz.my_dragon_list[SELECTED_DRAGON]["active"] == 'Y'):
                                print("Activate", SELECTED_DRAGON)
                                msg = font2.render(SELECTED_DRAGON_NAME + ' activated', True, (0, 0, 0))
                                msg_h = msg.get_rect().height
                                msg_w = msg.get_rect().width
                                store_area.blit(msg, ((AREA_WIDTH - msg_w) // 2, 40))
                                GameState.DRAGON = SELECTED_DRAGON_NAME
                            if (buy_btn.get_rect().collidepoint(x - AREA_LEFT - x_buy, y - AREA_TOP - y_buy)
                                    and Dragon_Quiz.my_dragon_list[SELECTED_DRAGON]["active"] == 'N'):
                                print("Buy", SELECTED_DRAGON)
                                if Dragon_Quiz.my_dragon_list[SELECTED_DRAGON]["price"] <= CURRENT_COINS:
                                    msg = font2.render(SELECTED_DRAGON_NAME + ' purchased', True, (0, 0, 0))
                                    Dragon_Quiz.my_dragon_list[SELECTED_DRAGON]["active"] = "Y"
                                    # Hide current coins value
                                    hide_old_coins()

                                    # Draw new coins value
                                    CURRENT_COINS = CURRENT_COINS - Dragon_Quiz.my_dragon_list[SELECTED_DRAGON]["price"]
                                    print(CURRENT_COINS)
                                    draw_new_coins()
                                    ##-----------------------------------------
                                else:
                                    msg = font2.render('Not enough coins to buy ' + SELECTED_DRAGON_NAME, True, (0, 0, 0))
                                msg_h = msg.get_rect().height
                                msg_w = msg.get_rect().width
                                store_area.blit(msg, ((AREA_WIDTH - msg_w) // 2, 40))
                            draw_dragon_shop()

                    if profie.get_rect().collidepoint(x - profile_x, y - profile_y):

                        file_name = Dragon_Quiz.my_dragon[GameState.DRAGON]['file']
                        img = pygame.transform.scale(load_image(file_name), (IMG_WIDTH, IMG_HEIGHT))
                        profile_area.blit(img, (10, 10))
                        #profile_area.blit(img, ((AREA_WIDTH-IMG_WIDTH)//2, (AREA_HEIGHT-IMG_HEIGHT)//2))

                        title = font1.render('Player1', True, (110, 52, 1))
                        title_height = title.get_rect().height
                        profile_area.blit(title, (5, IMG_HEIGHT + 15))
                        screen.blit(profile_area, (AREA_LEFT, AREA_TOP))
                        inLevel = False
                        inStore = False

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
                        inLevel = False
                        inStore = False

                    if choose_level.get_rect().collidepoint(x - choose_level_x, y - choose_level_y):
                        title = font1.render('Select level to continue:', True, (230, 0, 0))
                        title_height = title.get_rect().height
                        title_width = title.get_rect().width
                        choose_level_area.blit(title, ((AREA_WIDTH - title_width)//2, 5))
                        draw_levels()
                        inLevel = True
                        inStore = False
                    else:
                        if inLevel:
                            for i in range(len(levels)):
                                if levels[i]["image"].get_rect().collidepoint(x - AREA_LEFT - (winter_x + i * 120), y - AREA_TOP - winter_y):
                                    ACTIVE_LEVEL = i
                            draw_levels()
                    if play_btn.get_rect().collidepoint(x - play_btn_x, y - play_btn_y):
                        bonus = dragonfight.main(1)
                        if bonus == None:
                             bonus = 100
                        CURRENT_COINS += bonus
                    if quit_btn.get_rect().collidepoint(x - quit_btn_x, y - quit_btn_y):
                        inLevel = False
                        inStore = False
                        run = False
            #
            clock.tick(fps)
            pygame.display.flip()
            pygame.display.update()
        # завершение работы:
        pygame.quit()
