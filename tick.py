import pygame

lasttick = -1
tick = -1


def update_tick():
    global tick, lasttick
    lasttick = tick
    tick = pygame.time.get_ticks()


def get_diff():
    return tick - lasttick


def get_tick():
    return tick
