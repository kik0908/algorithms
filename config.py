import pygame
import pygame_gui

import timers


WIDTH = 1200
HEIGHT = 480
FPS = 6000

GUI_WIDTH = 250

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