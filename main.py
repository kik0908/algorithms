from random import shuffle

import pygame
import pygame_gui

from sorts import *
from utils import gradient_iter
import timers

WIDTH = 1000
HEIGHT = 480
FPS = 6000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TIMER_EVENT = 26

pygame.init()
gui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), './themes.json')
timer_manager = timers.TimerManager()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A")
clock = pygame.time.Clock()

sorts = {'Bubble sort': ('1', 20),
         "Sort by choice": ('2', 1),
         "Insertion sort": ('3', 20),
         "Lomuto`s quickSort": ('4', 20),
         "Hoare`s quickSort": ('5', 20)}

selector = pygame_gui.elements.ui_selection_list.UISelectionList(
    pygame.Rect((730, 0), (250, 30 * len(list(sorts.keys())))),
    list(sorts.keys()),
    gui_manager, allow_double_clicks=False)

animation_label = pygame_gui.elements.ui_label.UILabel(pygame.Rect((730, 440), (250, 30)),
                                                       "Animation delay is",
                                                       gui_manager, object_id="#just_text")
status_label_ok = pygame_gui.elements.ui_label.UILabel(pygame.Rect((730, 405), (250, 30)),
                                                       "Finished",
                                                       gui_manager, object_id='#finished')
status_label_in_process = pygame_gui.elements.ui_label.UILabel(pygame.Rect((730, 405), (250, 30)),
                                                               "In process",
                                                               gui_manager, object_id='#in_process')
status_label_ok.visible = False
status_label_in_process.visible = False
animation_label.visible = False

text_line_delay = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(pygame.Rect((730, 190), (250, 30)),
                                                                         gui_manager)

count = 90

color_min, color_max = (0, 127, 255), (204, 255, 51)
colors = list(gradient_iter(color_min, color_max, count))

array = [((i + 1) * 5, colors[i]) for i in range(count)]


def init_sorting(type, delay=20):
    timer = timers.Timer(timer_manager, pygame.event.Event(TIMER_EVENT, {'timer_id': 'sort'}), delay, id='sort')

    array = [((i + 1) * 5, colors[i]) for i in range(count)]
    shuffle(array)

    sorting = {'1': bubble_sort_iter(array, func=lambda x: x[0]),
               '2': sort_by_choice_iter(array, func=lambda x: x[0]),
               '3': insertion_sort_iter(array, func=lambda x: x[0]),
               '4': lomuto_quickSort_iter(array, 0, len(array) - 1, func=lambda x: x[0]),
               '5': hoare_quickSort_iter(array, 0, len(array) - 1, func=lambda x: x[0])}

    it = sorting[sorts[type][0]]

    return array, it


it = None

running = True
while running:
    time_delta = clock.tick(FPS) / 1000
    screen.fill(BLACK)
    timer_manager.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

        elif event.type == TIMER_EVENT:
            if event.timer_id == 'sort':
                try:
                    s_t = pygame.time.get_ticks()
                    array = next(it)
                    all_time += pygame.time.get_ticks() - s_t
                except StopIteration:
                    timer_manager.delete_timer('sort')
                    status_label_ok.visible = True
                    status_label_in_process.visible = False
                    status_label_ok.set_text(f"Finished in about {all_time / 1000}s")

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:

                timer_manager.delete_timer('sort')
                delay = sorts[event.text][1]
                if text_line_delay.get_text().isdigit() is True:
                    delay = int(text_line_delay.get_text())
                else:
                    text_line_delay.set_text(str(delay))

                array, it = init_sorting(event.text, delay)
                status_label_in_process.visible = True
                animation_label.visible = True
                animation_label.set_text(f"Animation delay is {delay}")

                all_time = 0

            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                timer: timers.Timer = timer_manager['sort']
                if timer is not None:
                    if text_line_delay.get_text().isdigit() is True:
                        delay = int(text_line_delay.get_text())
                        timer.new_delay(delay)
                        animation_label.set_text(f"Animation delay is {delay}")

        gui_manager.process_events(event)

    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)

    s = 8
    for ind, i in enumerate(array):
        pygame.draw.line(screen, i[1], (s + ind * s, HEIGHT), (s + ind * s, HEIGHT - i[0]), s - 1)

    pygame.display.flip()

pygame.quit()
