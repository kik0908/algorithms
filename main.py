import pygame
import pygame_gui
from random import shuffle, randint

from sorts import *
from utils import gradient_iter

WIDTH = 1000
HEIGHT = 480
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
manager = pygame_gui.UIManager((WIDTH, HEIGHT), './themes.json')

selector = pygame_gui.elements.ui_selection_list.UISelectionList(pygame.Rect((730, 0), (250,60)),
                                                                 ['test 1', 'test 2'],
                                                                 manager)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A")
clock = pygame.time.Clock()

count = 90

color_min, color_max = (0, 127, 255), (204, 255, 51)
colors = list(gradient_iter(color_min, color_max, count))

timer = None

a = pygame.time.set_timer(pygame.USEREVENT + 1, 20)
array = [((i + 1) * 5, colors[i]) for i in range(count)]
shuffle(array)

sorting = {'1': bubble_sort_iter(array, func=lambda x: x[0]),
           '2': sort_by_choice_iter(array, func=lambda x: x[0]),
           '3': insertion_sort_iter(array, func=lambda x: x[0]),
           '4': lomuto_quickSort_iter(array, 0, len(array) - 1, func=lambda x: x[0]),
           '5': hoare_quickSort_iter(array, 0, len(array) - 1, func=lambda x: x[0])}

it = sorting['3']

running = True
while running:
    time_delta = clock.tick(FPS) / 1000
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            try:
                array = next(it)
            except StopIteration:
                pass
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                print(event.text)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(screen)

    s = 8
    for ind, i in enumerate(array):
        pygame.draw.line(screen, i[1], (s + ind * s, HEIGHT), (s + ind * s, HEIGHT - i[0]), s - 1)

    pygame.display.flip()

pygame.quit()
