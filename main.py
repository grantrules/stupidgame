import logging

import pygame
from pygame.locals import *

from gamemenu import GameMenu
from title import Title

import gamesettings

logger = logging.getLogger(__name__)


game_title = "The Title of my Game"



def init_screen(width, height):
    return pygame.display.set_mode((width, height), pygame.RESIZABLE)


class GameRunner():

    def __init__(self, screen):
        self.screen = screen
        self.runner = Title(self, GameMenu(self, None), game_title)
        self.cur_time = 0

        gamesettings.load_settings()

    def run(self):
        """This is our app main loop"""
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
    import os.path
    import glob

    pygame.init()
    pygame.font.init()
    screen = init_screen(640,480)
    pygame.display.set_caption(game_title)
    logging.basicConfig(level=logging.DEBUG)

    # loop through a bunch of maps in the maps folder
    try:
        GameRunner(screen).run()
    except:
        pygame.quit()
        raise
