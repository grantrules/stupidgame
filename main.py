import logging

import pygame
from pygame.locals import *

from gamemenu import GameMenu
from title import Title
from screen import init_screen

import sound

import gamesettings

logger = logging.getLogger(__name__)


game_title = "The Title of my Game"


class GameRunner():

    def __init__(self, screen):
        self.screen = screen
        self.runner = Title(self, GameMenu(self, None), game_title)
        self.cur_time = 0

    def run(self):
        self.dirty = True
        self.running = True
        self.exit_status = 1

        while self.running:
            self.last_time = self.cur_time
            self.runner.cur_time = pygame.time.get_ticks()
            
            events = pygame.event.get()

            self.runner.handle_input(events)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if hasattr(self.runner, 'ingame') and self.runner.ingame:
                            self.runner = GameMenu(self, self.runner)
                if event.type == pygame.QUIT:
                    if event.type == QUIT:
                        self.exit_status = 0
                        self.running = False
                    elif event.type == VIDEORESIZE:
                        init_screen(event.w, event.h)

            self.runner.run()

            pygame.display.flip()

        return self.exit_status


if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    gamesettings.load_settings()

    screen = init_screen(640,480)
    pygame.display.set_caption(game_title)
    logging.basicConfig(level=logging.DEBUG)

    sound.initialize()

    # loop through a bunch of maps in the maps folder
    try:
        GameRunner(screen).run()
    except:
        pygame.quit()
        raise
