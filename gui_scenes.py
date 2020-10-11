from random import shuffle

import pygame
import pygame_gui

import timers
from sorts import *
from utils import gradient_iter
from config import *

sorts = {'Bubble sort': ('1', 20),
         "Sort by choice": ('2', 20),
         "Sort by double choice": ('3', 20),
         "Insertion sort": ('4', 20),
         "Lomuto`s quickSort": ('5', 20),
         "Hoare`s quickSort": ('6', 20),
         "Merge sort": ('7', 20),
         "Cocktail sort": ('8', 20)}

main_menu_topic = {"Sorts": lambda: Sorting(SceneManager)}


class SceneManager:
    def __init__(self):
        self.scenes = []
        self.active_scene = MainMenu(self)

    def add(self, scene):
        self.scenes.append(scene)

    def update(self):
        pass

    def check_event(self, event):
        self.active_scene.check_event(event)

    def render(self, screen):
        self.active_scene.render(screen)

    def set_scene(self, scene, delete_last=True):
        _ = self.active_scene
        _.deactivate()
        self.active_scene = scene
        if delete_last is True:
            del _



class Scene:
    def __init__(self, scene_manager):
        self.gui_elements = []
        self.is_active = True
        self.scene_manager = scene_manager

    def update(self):
        pass

    def check_event(self, event):
        pass

    def render(self, screen):
        pass

    def activate(self):
        self.is_active = True
        for i in self.gui_elements:
            i.visible = True

    def deactivate(self):
        self.is_active = False
        for i in self.gui_elements:
            i.visible = False
            i.kill()

        self.gui_elements.clear()


class Sorting(Scene):
    def __init__(self, scene_manager):
        super(Sorting, self).__init__(scene_manager)
        self.__init_gui()
        self.is_active = True

        self.count = 450
        self.element_h = 1

        self.steps_for_skip = 5

        self.color_min, color_max = (0, 127, 255), (204, 255, 51)
        self.colors = list(gradient_iter(self.color_min, color_max, self.count))

        self.array = [((i + 1) * self.element_h, self.colors[i]) for i in range(self.count)]

        self.it = None
        self.delay = 0

        self.all_time = 0

    def __init_gui(self):
        self.selector = pygame_gui.elements.ui_selection_list.UISelectionList(
            pygame.Rect((WIDTH - GUI_WIDTH, 0), (GUI_WIDTH, 30 * min(len(list(sorts.keys())), HEIGHT))),
            list(sorts.keys()),
            gui_manager, allow_double_clicks=False)

        self.animation_label = pygame_gui.elements.ui_label.UILabel(
            pygame.Rect((WIDTH - GUI_WIDTH, 440), (GUI_WIDTH, 30)),
            "Animation delay is",
            gui_manager, object_id="#just_text")
        self.status_label_ok = pygame_gui.elements.ui_label.UILabel(
            pygame.Rect((WIDTH - GUI_WIDTH, 405), (GUI_WIDTH, 30)),
            "Finished",
            gui_manager, object_id='#finished')
        self.status_label_in_process = pygame_gui.elements.ui_label.UILabel(
            pygame.Rect((WIDTH - GUI_WIDTH, 405), (GUI_WIDTH, 30)),
            "In process",
            gui_manager, object_id='#in_process')
        self.status_label_ok.visible = False
        self.status_label_in_process.visible = False
        self.animation_label.visible = False

        self.text_line_delay = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            pygame.Rect((WIDTH - GUI_WIDTH, 30 * len(list(sorts.keys())) + 10), (GUI_WIDTH, 30)),
            gui_manager)

        self.gui_elements.extend(
            [self.animation_label, self.status_label_ok, self.status_label_in_process, self.text_line_delay,
             self.selector])

    def update(self):
        pass

    def check_event(self, event):
        if self.is_active is True:
            if event.type == TIMER_EVENT:
                if event.timer_id == 'sort':
                    try:
                        if self.delay < 0:
                            for i in range(abs(self.delay) * self.steps_for_skip):
                                s_t = pygame.time.get_ticks()
                                self.array = next(self.it)
                                self.all_time += pygame.time.get_ticks() - s_t
                        else:
                            s_t = pygame.time.get_ticks()
                            self.array = next(self.it)
                            self.all_time += pygame.time.get_ticks() - s_t
                    except StopIteration:
                        timer_manager.delete_timer('sort')
                        self.status_label_ok.visible = True
                        self.status_label_in_process.visible = False
                        self.status_label_ok.set_text(f"Finished in about {self.all_time / 1000}s")

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    timer_manager.delete_timer('sort')
                    self.delay = sorts[event.text][1]
                    if self.text_line_delay.get_text().replace('-', '').isdigit() is True:
                        self.delay = int(self.text_line_delay.get_text())
                    else:
                        self.text_line_delay.set_text(str(self.delay))

                    self.array, self.it = self.init_sorting(event.text, self.delay)
                    self.status_label_in_process.visible = True
                    self.animation_label.visible = True
                    self.animation_label.set_text(f"Animation delay is {self.delay}")

                    self.all_time = 0

                elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    timer: timers.Timer = timer_manager['sort']
                    if timer is not None:
                        if self.text_line_delay.get_text().replace('-', '').isdigit() is True:
                            self.delay = int(self.text_line_delay.get_text())
                            timer.new_delay(self.delay)
                            self.animation_label.set_text(f"Animation delay is {self.delay}")

    def render(self, screen):
        if self.is_active is True:
            s = 2
            for ind, i in enumerate(self.array):
                pygame.draw.line(screen, i[1], (s + ind * s, HEIGHT), (s + ind * s, HEIGHT - i[0]), s - 1)

    def init_sorting(self, type, delay=20):
        timer = timers.Timer(timer_manager, pygame.event.Event(TIMER_EVENT, {'timer_id': 'sort'}), delay, id='sort')

        self.array = [((i + 1) * self.element_h, self.colors[i]) for i in range(self.count)]
        shuffle(self.array)
        func_for_sort = lambda x: x[0]

        sorting = {'1': lambda: bubble_sort_iter(self.array, func=func_for_sort),
                   '2': lambda: sort_by_choice_iter(self.array, func=func_for_sort),
                   '3': lambda: double_selection_sort_iter(self.array, func=func_for_sort),
                   '4': lambda: insertion_sort_iter(self.array, func=func_for_sort),
                   '5': lambda: lomuto_quickSort_iter(self.array, func=func_for_sort),
                   '6': lambda: hoare_quickSort_iter(self.array, func=func_for_sort),
                   '7': lambda: merge_sort_iter(self.array, func=func_for_sort),
                   '8': lambda: cocktail_sort_iter(self.array, func=func_for_sort)}

        it = sorting[sorts[type][0]]()

        return self.array, it


class MainMenu(Scene):
    def __init__(self, scene_manager):
        super(MainMenu, self).__init__(scene_manager)
        self.__init_gui()

    def __init_gui(self):
        self.selector = pygame_gui.elements.ui_selection_list.UISelectionList(
            pygame.Rect((WIDTH - GUI_WIDTH, 0), (GUI_WIDTH, min(30 * len(list(main_menu_topic.keys())), HEIGHT))),
            list(main_menu_topic.keys()),
            gui_manager, allow_double_clicks=False)

        self.gui_elements.extend([self.selector])

    def check_event(self, event):
        if self.is_active is True:
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    scene = event.text
                    self.scene_manager.set_scene(main_menu_topic[scene]())