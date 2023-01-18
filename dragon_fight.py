import os
import sys
import pygame as pg

FPS = 60
SPEED = 5   # Максимально плавное движение драконов
pg.init()
pg.display.set_caption('Dragon Power')
pg.key.set_repeat(1, 1)
sc = pg.display.set_mode((800, 450))
clock = pg.time.Clock()
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
tiles_group = pg.sprite.Group()
wall_group = pg.sprite.Group()
balls_group = pg.sprite.Group()
tile_images = {}


def terminate():
    pg.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as err:
        print('Cannot load image:', name)
        raise SystemExit(err)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


TILE_WIDTH = TILE_HEIGHT = 50
DRAGON_WIDTH = DRAGON_HEIGHT = 100


def load_level(filename):
    filename = "maps/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return [line.ljust(max_width, '.') for line in level_map]


def draw_bar(pos, color, f, mode):
    if mode == 1:
        pg.draw.rect(sc, pg.Color('black'), (*pos, 100, 20), 1)
        inner_pos = pos[0] + 3, pos[1] + 3
        inner_size = int(94 * f), 14
        pg.draw.rect(sc, color, (*inner_pos, *inner_size))
    elif mode == 2:
        pg.draw.rect(sc, pg.Color('black'), (*pos, 100, 20), 1)
        inner_pos = pos[0] + 3 + 94 - int(94 * f), pos[1] + 3
        inner_size = int(94 * f), 14
        pg.draw.rect(sc, color, (*inner_pos, *inner_size))
    else:
        raise SystemExit('Неправильный параметр mode')


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        if tile_type == 'empty':
            super().__init__(all_sprites, tiles_group)
        else:
            super().__init__(all_sprites, wall_group)
        self.image = pg.transform.scale(tile_images[tile_type], (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * x, TILE_HEIGHT * y)


class Ball(pg.sprite.Sprite):
    def __init__(self, coords, dir_, power, enemy):
        super().__init__(all_sprites, balls_group)
        dir_x, dir_y = dir_
        self.image = pg.transform.scale(fireball, (50, 50))
        self.rect = self.image.get_rect().move(*coords)
        self.mask = pg.mask.from_surface(self.image)
        self.vx = dir_x * 25
        self.vy = dir_y * 25
        self.power = power
        self.enemy = enemy

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        for wall in wall_group:
            if pg.sprite.collide_mask(self, wall):
                self.kill()
        if pg.sprite.collide_mask(self, self.enemy):
            self.enemy.damage(self.power)
            self.kill()


def generate_level(level):
    player1, player2, x, y = None, None, None, None
    coords1 = coords2 = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                if not any(coords1):
                    coords1 = x, y
                else:
                    coords2 = x, y
            elif level[y][x] == '#':
                Tile('wall', x, y)
    coords1, coords2 = sorted((coords1, coords2), key=lambda tpl: tpl[0])
    player1 = Dragon(3, *coords1, 'left')
    player2 = Dragon(3, *coords2, 'right')
    player1.set_enemy(player2)
    player2.set_enemy(player1)
    return player1, player2


class Dragon(pg.sprite.Sprite):
    def __init__(self, dragon_id, x, y, dir_):
        super().__init__(all_sprites, players_group)
        self.enemy = None
        self.dragon_id = dragon_id
        if dragon_id == 1:
            pic = air_dragon
            self.hp = self.max_hp = 700
        elif dragon_id == 2:
            pic = earth_dragon
            self.hp = self.max_hp = 1200
        elif dragon_id == 3:
            pic = fire_dragon
            self.hp = self.max_hp = 1000
        elif dragon_id == 4:
            pic = water_dragon
            self.hp = self.max_hp = 900
        else:
            raise SystemExit('Ошибка при вызове класса Dragon')
        self.image = pg.transform.scale(pic, (DRAGON_WIDTH, DRAGON_HEIGHT))
        self.rect = self.image.get_rect().move(TILE_WIDTH * x - 25, TILE_HEIGHT * y - 25)
        self.mask = pg.mask.from_surface(self.image)
        if dir_ == 'left':
            self.side_x = 1
        elif dir_ == 'right':
            self.side_x = -1
            self.image = pg.transform.flip(self.image, True, False)
        else:
            raise SystemExit('Ошибка при вызове класса Dragon')
        self.dir_x = 0
        self.dir_y = 0
        self.last_move_dir = 0, 0

    def update(self, dir_x, dir_y):
        dx = SPEED * dir_x
        dy = SPEED * dir_y
        self.rect.x += dx
        self.rect.y += dy
        if any(pg.sprite.collide_mask(self, sprite) for sprite in wall_group.sprites()) or \
                pg.sprite.collide_mask(self, self.enemy):
            self.rect.x -= dx
            self.rect.y -= dy
        if self.side_x == -dir_x:
            self.image = pg.transform.flip(self.image, True, False)
            self.mask = pg.mask.from_surface(self.image)
            self.side_x = dir_x
        self.dir_x = dir_x
        self.dir_y = dir_y
        if dir_x or dir_y:
            self.last_move_dir = dir_x, dir_y

    def set_enemy(self, other):
        if not isinstance(other, Dragon):
            raise TypeError
        self.enemy = other

    def attack(self):
        if self.hp == 0:
            return None
        if self.dragon_id == 1:
            if self.side_x == 1:
                x0 = self.rect.x + 75
            else:
                x0 = self.rect.x - 25
            y0 = self.rect.y + 20
            power = 125
        elif self.dragon_id == 2:
            if self.side_x == 1:
                x0 = self.rect.x + 50
            else:
                x0 = self.rect.x - 50
            y0 = self.rect.y + 10
            power = 200
        elif self.dragon_id == 3:
            if self.side_x == 1:
                x0 = self.rect.x + 65
            else:
                x0 = self.rect.x - 35
            y0 = self.rect.y - 5
            power = 175
        elif self.dragon_id == 4:
            if self.side_x == 1:
                x0 = self.rect.x + 75
            else:
                x0 = self.rect.x - 25
            y0 = self.rect.y + 5
            power = 150
        else:
            raise SystemExit('Неправильный dragon_id')
        if self.dir_x == 0 and self.dir_y == 0:
            if not any(self.last_move_dir):
                dir_x = self.side_x
                dir_y = 0
            else:
                dir_x, dir_y = self.last_move_dir
        else:
            dir_x = self.dir_x
            dir_y = self.dir_y
        Ball((x0, y0), (dir_x, dir_y), power, self.enemy)

    def damage(self, power):
        if power >= self.hp:
            self.die()
        else:
            self.hp -= power

    def get_hp(self):
        return self.hp / self.max_hp

    def die(self):
        self.hp = 0
        self.kill()


air_dragon = load_image('air_dragon.png')
earth_dragon = load_image('earth_dragon.png')
fire_dragon = load_image('fire_dragon.png')
water_dragon = load_image('water_dragon.png')
fireball = load_image('fireball.png')


def main(level_num):
    global tile_images
    if level_num == 1:
        level = 'map1.txt'
        tile_images = {
            'wall': load_image('bricks.jpg'),
            'empty': load_image('snow.jpg')
        }
    elif level_num == 2:
        level = 'map2.txt'
        tile_images = {
            'wall': load_image('bricks.jpg'),
            'empty': load_image('snow.jpg')
        }
    elif level_num == 3:
        level = 'map3.txt'
        tile_images = {
            'wall': load_image('box.png'),
            'empty': load_image('grass.png')
        }
    else:
        raise SystemExit('')
    player1, player2 = generate_level(load_level(level))
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
            if event.type == pg.MOUSEBUTTONUP:
                player1.attack()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    player2.attack()
        dx1 = dx1 / abs(dx1) if dx1 else 0
        dy1 = dy1 / abs(dy1) if dy1 else 0
        dx2 = dx2 / abs(dx2) if dx2 else 0
        dy2 = dy2 / abs(dy2) if dy2 else 0
        tiles_group.draw(sc)
        wall_group.draw(sc)
        players_group.draw(sc)
        balls_group.draw(sc)
        player1.update(dx1, dy1)
        player2.update(dx2, dy2)
        if balls_group.sprites():
            balls_group.update()
        draw_bar((30, 20), pg.Color('red'), player1.get_hp(), 1)
        draw_bar((670, 20), pg.Color('blue'), player2.get_hp(), 2)
        pg.display.flip()
        clock.tick(FPS)
