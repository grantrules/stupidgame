import pygame

from gamesettings import settings, register_setting_change_handler

sound_cache = {}

music_cache = {}

def initialize():
    pygame.mixer.init(11025)

def play_music(name):
    pygame.mixer.music.set_volume(1.0*(settings['music_volume']/10))
    pygame.mixer.music.load("snd/music/"+name+".mp3")
    pygame.mixer.music.play()


def play_sound(name):
    pass

def set_music_volume(value):
    pygame.mixer.music.set_volume(1.0*(value/10))

register_setting_change_handler('music_volume', set_music_volume)
