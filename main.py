from config import *
from gui_scenes import Sorting, SceneManager
scene = SceneManager()

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

        scene.check_event(event)

        gui_manager.process_events(event)

    gui_manager.update(time_delta)
    gui_manager.draw_ui(screen)

    scene.render(screen)

    pygame.display.flip()

pygame.quit()
