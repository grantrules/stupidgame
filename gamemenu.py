import pygame

from gameplay import GamePlay
from gamesettings import GameSettings
from gamequit import GameQuit
from about import About

from sound import play_music

from fonts import register_font, fonts


def load_resources():
    fontpath = "gfx/Acme-Regular.ttf"
    register_font("menu", fontpath, 40)


inactive = (255, 255, 255)
active = (255, 0, 0)


class MenuItem:
    def __init__(self, name, runner):
        self.name = name
        self.runner = runner


menu = [
    MenuItem("start", GamePlay),
    MenuItem("settings", GameSettings),
    MenuItem("about", About),
    MenuItem("quit", GameQuit),
]


class GameMenu:
    def __init__(self, gamerunner, lastrunner):
        self.screen = gamerunner.screen
        self.gamerunner = gamerunner
        self.lastrunner = lastrunner
        self.paused = bool(lastrunner)
        self.dirty = True
        self.font = fonts.get("menu")
        self.selected = 0
        self.lastkeys = []
        play_music("title")

    def run(self):
        if self.dirty:
            self.screen.fill((0, 0, 0))
            for x, item in enumerate(menu):
                ren = self.font.render(
                    item.name, 1, active if self.selected == x else inactive
                )
                self.screen.blit(
                    ren,
                    (
                        self.screen.get_width() / 2 - ren.get_width() / 2,
                        x * ren.get_height() + 10,
                    ),
                )
            self.dirty = False

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(menu)
                    self.dirty = True
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(menu)
                    self.dirty = True
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    if self.paused and self.selected == 0:
                        self.gamerunner.runner = self.lastrunner
                    if event.key == pygame.K_RETURN:
                        self.gamerunner.runner = menu[self.selected].runner(
                            self.gamerunner, self
                        )
                    self.dirty = True
