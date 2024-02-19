import pygame

from gamemenudialog import GameMenuDialog as Dialog

class GameQuit:
    def __init__(self, gamerunner, lastrunner):
        self.screen = gamerunner.screen
        self.gamerunner = gamerunner
        self.lastrunner = lastrunner
        
        def on_yes():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        def on_no():
            self.gamerunner.runner = self.lastrunner

        self.quitdialog = Dialog("Are you sure you'd like to quit?", on_yes, on_no)

    def run(self):
        self.quitdialog.draw(self.screen)

    def handle_input(self, events):
        self.quitdialog.handle_input(events)