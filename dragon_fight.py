import os
import sys
import pygame as pg

FPS = 60
SIZE = WIDTH, HEIGHT = 600, 480
STEP = 1   # Максимально плавное движение драконов
SPEED = 100  # Пикселей в секунду


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
DRAGON_IMAGE1 = load_image('none')   # Жду моделек
DRAGON_IMAGE2 = load_image('none')


class Dragon(pg.sprite.Sprite):
    def __init__(self, *args):
        groups = args[:-1]
        dragon_num = args[-1]
        super().__init__(*groups)
        if dragon_num == 1:
            self.image = DRAGON_IMAGE1
        else:
            self.image = DRAGON_IMAGE2
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def move(self, direction):
        dx = direction[0] * SPEED
        dy = direction[1] * SPEED
        self.rect = self.rect.move(dx, dy)


def main():
    pg.init()
    pg.key.set_repeat(200, 70)
    sc = pg.display.set_mode(SIZE)
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    players_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()
    player1 = Dragon(all_sprites, players_group, 1)
    player2 = Dragon(all_sprites, players_group, 2)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.K_w:
                player1.move((0, -1))
            if event.type == pg.K_a:
                player1.move((-1, 0))
            if event.type == pg.K_s:
                player1.move((0, 1))
            if event.type == pg.K_d:
                player1.move((1, 0))
            if event.type == pg.K_UP:
                player2.move((0, 1))
            if event.type == pg.K_LEFT:
                player2.move((-1, 0))
            if event.type == pg.K_DOWN:
                player2.move((0, 1))
            if event.type == pg.K_RIGHT:
                player2.move((1, 0))

