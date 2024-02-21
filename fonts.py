import pygame

fonts = {}


def register_font(name, path, size):
    fonts[name] = pygame.font.Font(path, size)
