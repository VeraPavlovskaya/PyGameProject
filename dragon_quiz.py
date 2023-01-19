import os
import random
import sys
import pygame
import dragon_fight

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
dragon_id = 0

questions = []

my_dragon = {'Earth': {'score': 130, 'name': 'earth', 'file': 'earth_dragon.png'},
             'Air': {'score': 180, 'name': 'air', 'file': 'air_dragon.png'},
             'Water': {'score': 230, 'name': 'water', 'file': 'water_dragon.png'},
             'Fire': {'score': 280, 'name': 'fire', 'file': 'fire_dragon.png'}}
my_dragon_list = [{"name": "Earth", "file": 'earth_dragon.png', "image": None, "price": 0, "active": "Y"},
                  {"name": "Air", "file": 'air_dragon.png', "image": None, "price": 0, "active": "Y"},
                  {"name": "Fire", "file": 'fire_dragon.png', "image": None, "price": 1000, "active": "N"},
                  {"name": "Water", "file": 'water_dragon.png', "image": None, "price": 0, "active": "Y"}
                  ]


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


class SimpleScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((650, 480))
        self.background.fill(pygame.Color('lightgreen'))
        fon = pygame.transform.scale(load_image('picture_dragons.jpg'), (650, 480))
        self.background.blit(fon, (0, 0))
        y = 80
        if text:
            if SimpleScene.FONT is None:
                SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
            i = 0
            for line in text:
                i += 1
                text_rect = SimpleScene.FONT.get_rect(line)
                text_rect.center = self.background.get_rect().center
                text_rect = (text_rect[0], text_rect[1] + 20 * i, text_rect[2], text_rect[3])
                print(text_rect)
                SimpleScene.FONT.render_to(self.background, text_rect, line, pygame.Color('white'))
                # SimpleScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                # SimpleScene.FONT.render_to(self.background, (119, y - 1), line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text
        image_d = pygame.image.load('images/picture_dragons.jpg')
        # image_d.convert(SimpleScene)

    def draw(self):
        screen.blit(self.background, (0, 0))
        # if self.additional_text:
        #    print("additional_text")
        #    y = 180
        #    for line in self.additional_text:
        #        SimpleScene.FONT.render_to(screen, (120, y), line, pygame.Color('black'))
        #        SimpleScene.FONT.render_to(screen, (119, y - 1), line, pygame.Color('white'))
        #        y += 10

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.next_scene == 'GAME':
                    return 'GAME', GameState(0)
                return self.next_scene, None


##########
class FinalScene:
    FONT = None

    def __init__(self, next_scene, *text):
        self.background = pygame.Surface((650, 480))
        self.background.fill(pygame.Color('lightgreen'))
        fon = pygame.transform.scale(load_image('bg.jfif'), (650, 480))
        self.background.blit(fon, (0, 0))
        y = 80
        if text:
            if FinalScene.FONT is None:
                FinalScene.FONT = pygame.freetype.SysFont(None, 32)
            i = 0
            for line in text:
                i += 1
                text_rect = FinalScene.FONT.get_rect(line)
                text_rect.center = self.background.get_rect().center
                text_rect = (text_rect[0], text_rect[1] - 140 * i, text_rect[2], text_rect[3])
                print("FinalScene:", text_rect)
                print("FinalScene:", line)
                FinalScene.FONT.render_to(self.background, text_rect, line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text
        self.draw()
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    flag = False
                    break
            pygame.display.flip()
        dragon_fight.main(random.randint(1, 3), dragon_id)

    def draw(self):
        screen.blit(self.background, (0, 0))
        if self.additional_text:
            y = 180
            for line in self.additional_text:
                SimpleScene.FONT.render_to(screen, (120, y), line, pygame.Color('black'))
                SimpleScene.FONT.render_to(screen, (119, y - 1), line, pygame.Color('white'))
                y += 50

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.next_scene == 'GAME':
                    return 'GAME', GameState(0)
                return self.next_scene, None


class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = [
            ["What is your eye color?", ["Blue", "Green", "Gray", "Brown"]],
            ["What is your zodiac sign?",
             ["Sagittarius, Leo, Aries", "Taurus, Virgo, Capricorn", "Pisces, Scorpio, Cancer",
              "Libra, Aquarius, Gemini"]],
            ["Your friends say that you are", ["Joyful and optimistic", "Smart and ambitious", "Creative and emotional",
                                               "peaceful and kind"]],
            ["What do you usually do in your freetime?", ["I do sports", "I prefer reading", "I sing or dance",
                                                          "All of the above"]],
            ["What are your favorite school subjects?", ["I love exact sciences", "I love languages and literature",
                                                         "PE is the best!", "I'm not sure"]],
            ["What creatures do you like the most?", ["Pets", "Extinct animals", "Mythical creatures", "Wild animals"]],
            ["Where do you feel more comfortable?", ["I enjoy going to the mountains", "I like going the beach",
                                                     "I feel better at the city centre", "I choose the forests"]]
        ]
        self.current_question = None
        self.right = 0
        self.wrong = 0

    def pop_question(self):
        q = random.choice(self.questions)
        self.questions.remove(q)
        self.current_question = q
        return q

    def answer(self, answer):
        self.right += 1

    def get_result(self):
        global dragon_id
        dragon = self.get_dragon()
        dragon_id = {'Air': 1, 'Earth': 2, 'Fire': 3, 'Water': 4}[dragon]
        print(dragon)
        # if dragon == 'Water dragon':
        return f'{dragon} dragon', '', f'You have {self.right} points', '', 'Press any key to start!'

    def get_dragon(self):
        if 0 < self.right <= my_dragon['Earth']['score']:
            GameState.DRAGON = 'Earth'
            return 'Earth'
        elif my_dragon['Earth']['score'] < self.right <= my_dragon['Air']['score']:
            GameState.DRAGON = 'Air'
            return 'Air'
        elif my_dragon['Air']['score'] < self.right <= my_dragon['Water']['score']:
            GameState.DRAGON = 'Water'
            return 'Water'
        else:
            GameState.DRAGON = 'Fire'
            return 'Fire'


class SettingScene:

    def __init__(self):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgreen'))
        if SimpleScene.FONT is None:
            SimpleScene.FONT = pygame.freetype.SysFont('arial.ttf', 32)
        self.rects = []
        x = 120
        y = 120
        for n in range(4):
            rect = pygame.Rect(x, y, 20000, 80)
            self.rects.append(rect)
            y += 100

    def start(self, *args):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgrey'), rect)
            pygame.draw.rect(screen, pygame.Color('blue'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 30), str(n), pygame.Color('black'))
            SimpleScene.FONT.render_to(screen, (rect.x + 29, rect.y + 29), str(n), pygame.Color('white'))
            n += 1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        return 'GAME', GameState(n)
                    n += 1


class GameScene:
    def __init__(self):
        print(SimpleScene.FONT)
        # if SimpleScene.FONT == None:
        SimpleScene.FONT = pygame.freetype.SysFont('arial.ttf', 28)
        self.background = None
        self.gamestate = None
        # Важное место! Устонавливаем размеры боксов
        SimpleScene.FONT = pygame.freetype.SysFont(None, 28)
        SimpleScene.FONT = pygame.freetype.SysFont(None, 28)
        self.rects = []
        x = 20
        y = 120
        for n in range(4):
            rect = pygame.Rect(x, y, 600, 80)
            self.rects.append(rect)
            y += 80

    # Боксы с вариантами ответов
    def start(self, gamestate):
        x0 = 50
        y0 = 120
        self.background = pygame.Surface((640, 1000))
        self.background.fill((23, 23, 23))
        self.gamestate = gamestate
        question, answer = gamestate.pop_question()
        SimpleScene.FONT.render_to(self.background, (x0, 49), question, pygame.Color('white'))
        x = 100
        y = 150
        for i in range(4):
            SimpleScene.FONT.render_to(self.background, (x, y), answer[i], pygame.Color('white'))
            y += 80

    def draw(self):
        screen.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, pygame.Color('darkgreen'), rect, 5)
            SimpleScene.FONT.render_to(screen, (rect.x + 30, rect.y + 30), str(n), pygame.Color('white'))
            n += 1

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        self.gamestate.answer(n)
                        if self.gamestate.questions:
                            return 'GAME', self.gamestate
                        else:
                            return 'RESULT', self.gamestate.get_result()


def main():
    global dragon_id
    dt = 0
    scenes = {
        'TITLE': SimpleScene('GAME', '', '', '', '', '', '', 'Welcome to the Dragon Land!', '',
                             'press any button to start the quiz'),
        # 'SETTING': SettingScene(),
        'GAME': GameScene(),
        'RESULT': FinalScene('TITLE', 'Here is your result:'),
    }
    scene = scenes['TITLE']
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)
                if isinstance(scene, FinalScene):
                    return None

        scene.draw()
        pygame.display.flip()
        dt = clock.tick(60)


if __name__ == '__main__':
    main()
