import pygame

pygame.init()


class TimerManager:
    def __init__(self):
        self.timers = {}
        self.count = 0

    def add(self, other, num=None):
        if num in self.timers:
            raise IndexError("This id in timers")
        if num is None:
            self.timers[self.count] = other
        else:
            self.timers[num] = other
        self.count += 1
        return self.count - 1

    def update(self):
        for_del = []
        for_del_c = 0
        for ind, timer in enumerate(self.timers.items()):
            if timer[1].check() is True:
                _ = pygame.event.Event(26, timer_id = timer[0])
                pygame.event.post(timer[1].event)
                if timer[1].for_del is True:
                    for_del.append(ind)
                    for_del_c += 1

        self.count -= for_del_c
        for i in for_del:
            self.timers.pop(i)

    def delete_timer(self, id):
        if id in self.timers:
            del self.timers[id]
            self.count -= 1

    def __getitem__(self, id):
        return self.timers.get(id, None)


class Timer:
    def __init__(self, timer_manager, event, delay, id=None, once=False):

        self.event = event
        self.delay = delay
        self.once = once
        self.last_time = pygame.time.get_ticks()
        self.for_del = False
        self.id = id

        timer_manager.add(self, id)

    def check(self):
        if self.for_del is False:
            if pygame.time.get_ticks() - self.last_time > self.delay:
                self.last_time = pygame.time.get_ticks()
                if self.once is True:
                    self.delete()
                return True
            return False
        return False

    def delete(self):
        self.for_del = True

    def new_delay(self, new_delay):
        self.delay = new_delay


class TimerTime:
    def __init__(self, time):
        self.time = time
        self.start_time = pygame.time.get_ticks()

    def check(self):
        if pygame.time.get_ticks() - self.start_time > self.time:
            return True

        return False
