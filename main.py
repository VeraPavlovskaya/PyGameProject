import pygame

if __name__ == '__main__':
    # инициализация Pygame:
    width = 700
    height = 750
    print('Неправильный формат ввода')
    exit()
    pygame.init()
    # размеры окна:
    white = [255, 255, 255]
    pygame.display.set_caption('Шахматы')
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode((width, height))
