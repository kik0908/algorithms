import pygame
from random import shuffle, randint

from sorts import *
from utils import gradient_iter

WIDTH = 720
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A")
clock = pygame.time.Clock()

count = 50

colors = list(gradient_iter((255, 126, 65), (56, 155, 255), count))

a = pygame.time.set_timer(pygame.USEREVENT, 20)
array = [((i + 1) * 7, colors[i]) for i in range(count)]
shuffle(array)
it = bubble_sort_iter(array, func=lambda x: x[0])
it = sort_by_choice_iter(array, func=lambda x: x[0])
it = insertion_sort_iter(array, func=lambda x: x[0])

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            try:
                array = next(it)
            except StopIteration:
                pass

    s = 10
    for ind, i in enumerate(array):
        pygame.draw.line(screen, i[1], (s + ind * s, 400), (s + ind * s, 400 - i[0]), 8)

    pygame.display.flip()

pygame.quit()
