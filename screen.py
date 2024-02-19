import pygame

from gamesettings import settings


def init_screen(width, height):
    return pygame.display.set_mode((width, height), pygame.SCALED)