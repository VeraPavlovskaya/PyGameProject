import os
import sys
import pygame as pg

FPS = 60
SPEED = 1   # Максимально плавное движение драконов
pg.init()
pg.key.set_repeat(1, 1)
sc = pg.display.set_mode((800, 450))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()


def terminate():
    pg.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


TILE_IMAGES = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
TILE_WIDTH = TILE_HEIGHT = 50
DRAGON_WIDTH = DRAGON_HEIGHT = 75


def load_level(filename):
    filename = "maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return [line.ljust(max_width, '.') for line in level_map]


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = pg.transform.scale(TILE_IMAGES[tile_type], (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * x, TILE_HEIGHT * y)


def generate_level(level):
    player1, player2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                if player1:
                    player2 = Dragon(2, x, y, 'right')
                else:
                    player1 = Dragon(1, x, y, 'left')
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return player1, player2


class Dragon(pg.sprite.Sprite):
    def __init__(self, dragon_id, x, y, dir_):
        super().__init__(all_sprites, players_group)
        if dragon_id == 1:
            pic = air_dragon
        elif dragon_id == 2:
            pic = earth_dragon
        elif dragon_id == 3:
            pic = fire_dragon
        elif dragon_id == 4:
            pic = water_dragon
        else:
            raise SystemExit('Ошибка при вызове класса Dragon')
        self.image = pg.transform.flip(pg.transform.scale(pic, (DRAGON_WIDTH, DRAGON_HEIGHT)), True, False)
        self.rect = self.image.get_rect().move(TILE_WIDTH * x - 25, TILE_HEIGHT * y - 25)
        if dir_ == 'left':
            self.dir = 1
        elif dir_ == 'right':
            self.dir = -1
        else:
            raise SystemExit('Ошибка при вызове класса Dragon')

    def update(self, dir_x, dir_y):
        self.rect.x += SPEED * dir_x
        if (self.dir == 1 and dir_x == -1) or (self.dir == -1 and dir_x == 1):
            self.image = pg.transform.flip(self.image, True, False)
            self.dir *= -1
        self.rect.y += SPEED * dir_y


air_dragon = load_image('Fire_Dragon.jpg')
earth_dragon = load_image('Earth_Dragon2.jpg')
fire_dragon = load_image('Fire_Dragon.jpg')
water_dragon = load_image('Water_dragon.png')


def main():
    player1, player2 = generate_level(load_level('map1.txt'))
    while True:
        dx1 = dy1 = dx2 = dy2 = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                pressed_keys = pg.key.get_pressed()
                if pressed_keys[pg.K_w]:
                    dy1 -= 1
                if pressed_keys[pg.K_a]:
                    dx1 -= 1
                if pressed_keys[pg.K_s]:
                    dy1 += 1
                if pressed_keys[pg.K_d]:
                    dx1 += 1
                if pressed_keys[pg.K_UP]:
                    dy2 -= 1
                if pressed_keys[pg.K_LEFT]:
                    dx2 -= 1
                if pressed_keys[pg.K_DOWN]:
                    dy2 += 1
                if pressed_keys[pg.K_RIGHT]:
                    dx2 += 1
        player1.update(dx1, dy1)
        player2.update(dx2, dy2)
        tiles_group.draw(sc)
        players_group.draw(sc)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()