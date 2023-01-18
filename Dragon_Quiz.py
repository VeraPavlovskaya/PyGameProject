import pygame
import pygame.freetype
import random
import os
import sys

questions = []

my_dragon = {'Earth': {'score': 130, 'name': 'earth', 'file': 'earth_Dragon.png'},
             'Air': {'score': 180, 'name': 'air', 'file': 'air_Dragon.png'},
             'Water': {'score': 230, 'name': 'water', 'file': 'Water_dragon.png'},
             'Fire': {'score': 280, 'name': 'fire', 'file': 'fire_Dragon.png'}}
my_dragon_list = ['earth_Dragon.png', 'air_Dragon.png', 'Water_dragon.png', 'fire_Dragon.png']

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
        fon = pygame.transform.scale(load_image('bg.jfif'), (650, 480))
        self.background.blit(fon, (0, 0))
        y = 80
        if text:
            if SimpleScene.FONT == None:
                SimpleScene.FONT = pygame.freetype.SysFont(None, 32)
            i = 0
            for line in text:
                i += 1
                text_rect = SimpleScene.FONT.get_rect(line)
                text_rect.center = self.background.get_rect().center
                text_rect = (text_rect[0], text_rect[1] - 40 * i, text_rect[2], text_rect[3])
                print(text_rect)
                print(line)
                SimpleScene.FONT.render_to(self.background, text_rect, line, pygame.Color('white'))
                # SimpleScene.FONT.render_to(self.background, (120, y), line, pygame.Color('black'))
                # SimpleScene.FONT.render_to(self.background, (119, y - 1), line, pygame.Color('white'))
                y += 50

        self.next_scene = next_scene
        self.additional_text = None

    def start(self, text):
        self.additional_text = text
        image_d = pygame.image.load('picture_dragons.jpg')
        # image_d.convert(SimpleScene)

    def draw(self, screen):
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
                    return ('GAME', GameState(0))
                return (self.next_scene, None)


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
            if FinalScene.FONT == None:
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
        image_d = pygame.image.load('picture_dragons.jpg')
        # image_d.convert(SimpleScene)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        if self.additional_text:
            y = 320
            i = 0
            for line in self.additional_text:
                i += 1
                FinalScene.FONT.render_to(screen, (160, y), line, pygame.Color('black'))
                FinalScene.FONT.render_to(screen, (159, y - 1), line, pygame.Color('white'))
                #
                y += 20
            file_name = my_dragon[GameState.DRAGON]['file']
            img = pygame.transform.scale(load_image(file_name), (120, 120))
            screen.blit(img, (250, 170))

    def update(self, events, dt):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.next_scene == 'GAME':
                    return ('GAME', GameState(0))
                return (self.next_scene, None)


##########

class GameState:
    DRAGON = 'Air'
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.questions = [
            ["What is your eye color?", ["Blue", "Green", "Gray", "Brown"], [10, 20, 30, 40]],
            ["What is your zodiac sign?",
             ["Sagittarius, Leo, Aries", "Taurus, Virgo, Capricorn", "Pisces, Scorpio, Cancer",
              "Libra, Aquarius, Gemini"], [40, 20, 30, 10]],
            ["Your friends say that you are", ["Joyful and optimistic", "Smart and ambitious", "Creative and emotional",
                                               "peaceful and kind"], [20, 30, 10, 40]],
            ["What do you usually do in your freetime?", ["I do sports", "I prefer reading", "I sing or dance",
                                                          "All of the above"], [30, 40, 20, 10]],
            ["What are your favorite school subjects?", ["I love exact sciences", "I love languages and literature",
                                                         "PE is the best!", "I'm not sure"], [10, 20, 30, 40]],
            ["What creatures do you like the most?", ["Pets", "Extinct animals", "Mythical creatures", "Wild animals"],
             [10, 20, 30, 40]],
            ["Where do you feel more comfortable?", ["I enjoy going to the mountains", "I like going the beach",
                                                     "I feel better at the city centre", "I choose the forests"],
             [10, 20, 30, 40]]
        ]
        self.current_question = None
        self.right = 0

    def pop_question(self):
        q = random.choice(self.questions)
        self.questions.remove(q)
        self.current_question = q
        return q

    def answer(self, points):
        self.right += points

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

    def get_result(self):
        dragon = self.get_dragon()
        print(dragon)
        # if dragon == 'Water dragon':
        return f'{dragon} dragon', '', f'You have {self.right} points', '', 'Press any key to start!'


'''class SettingScene:

    def __init__(self):
        self.background = pygame.Surface((640, 480))
        self.background.fill(pygame.Color('lightgreen'))

        if SimpleScene.FONT == None:
            SimpleScene.FONT = pygame.freetype.SysFont(None, 32)

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
                        return ('GAME', GameState(n))
                    n += 1'''


class GameScene:
    def __init__(self):
        print(SimpleScene.FONT)
        # if SimpleScene.FONT == None:
        SimpleScene.FONT = pygame.freetype.SysFont(None, 28)
        # Важное место! Устонавливаем размеры боксов
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
        question, answer, self.points = gamestate.pop_question()
        SimpleScene.FONT.render_to(self.background, (x0, 49), question, pygame.Color('white'))
        x = 100
        y = 150
        for i in range(4):
            SimpleScene.FONT.render_to(self.background, (x, y), answer[i], pygame.Color('white'))
            y += 80

    def draw(self, screen):
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
                for num, rect in enumerate(self.rects):
                    if rect.collidepoint(event.pos):
                        self.gamestate.answer(self.points[num])
                        print(self.points[num])
                        if self.gamestate.questions:
                            return ('GAME', self.gamestate)
                        else:
                            return ('RESULT', self.gamestate.get_result())


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    dt = 0
    scenes = {
        'TITLE': SimpleScene('GAME', 'Press any button to start the quiz', 'Welcome to the Dragon Land!'),
        # 'SETTING': SettingScene(),
        'GAME': GameScene(),
        'RESULT': FinalScene('TITLE', 'Here is your result:'),
    }
    scene = scenes['TITLE']
    while True:
        events = pygame.event.get()
        for e in events:
            if (e.type == pygame.QUIT
               or (e.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN] and scene == scenes['RESULT'])):
                return

        result = scene.update(events, dt)
        if result:
            next_scene, state = result
            if next_scene:
                scene = scenes[next_scene]
                scene.start(state)

        scene.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60)


if __name__ == '__main__':
    main()
