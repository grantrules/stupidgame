import pygame, logging

from sprites import Sprites
from gamerenderer import GameRenderer
from player import Player

from tick import get_diff

from input import keys

logger = logging.getLogger(__name__)

map = "gfx/basic.tmx"

class GamePlay:
    def __init__(self, gamerunner, lastrunner):
        self.screen = gamerunner.screen
        self.gamerunner = gamerunner
        self.renderer = None
        self.running = False
        self.moving = False
        self.dirty = False
        self.exit_status = 0

        self.sprites = Sprites()
        self.cur_time = 0
        self.camerax = 0
        self.cameray = 0
        self.pos = (0, 0)
        self.ingame = True
        self.window = (100, 100)
        self.load_map(map)


        self.players = [Player(self.sprites, self.renderer)]

    def load_map(self, filename) -> None:
        """Create a renderer, load data, and print some debug info"""
        self.renderer = GameRenderer(filename, self, self.window)

    def draw(self, surface) -> None:

        temp = pygame.Surface(size=(640, 480))

        self.renderer.update_window()

        # render the map onto the temporary surface
        self.renderer.render_map(temp)

        # now resize the temporary surface to the size of the display
        # this will also 'blit' the temp surface to the display
        pygame.transform.smoothscale(temp, surface.get_size(), surface)


    def run(self) -> None:
        movement = (0, 0)
        if self.moving:
            for key, (movx, movy) in keys.items():
                if self.keys[key]:
                    (x, y) = movement
                    movement = (x + movx, y + movy)
        self.players[0].move(movement, get_diff())

        self.draw(self.screen)

    def handle_input(self, events) -> None:

        self.keys = pygame.key.get_pressed()

        self.moving = False
        for k in keys.keys():
            if self.keys[k]:
                self.moving = True
                break
