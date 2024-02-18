import pygame


def init_screen(width, height):
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)