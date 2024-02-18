import pygame

from gamesettings import settings

sound_cache = {}

music_cache = {}

def handle_settings_change():
    pygame.mixer.music.set_volume(1.0*(settings['music_volume']/10))
    
def initialize():
    pygame.mixer.init(11025)

def play_music(name):
    print(settings)
    pygame.mixer.music.set_volume(1.0*(settings['music_volume']/10))
    pygame.mixer.music.load("snd/music/"+name+".mp3")
    pygame.mixer.music.play()


def play_sound(name):
    pass