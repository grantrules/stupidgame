import pygame, logging

from sprites import Sprites
from tiled import TiledRenderer
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

        self.load_map(map)
        self.sprites = Sprites()
        self.cur_time = 0
        self.camerax = 0
        self.cameray = 0
        self.pos = (0, 0)
        self.ingame = True
        self.window = (100, 100)

        self.player = Player(self.sprites, self.renderer)

    def load_map(self, filename) -> None:
        """Create a renderer, load data, and print some debug info"""
        self.renderer = TiledRenderer(filename)

        logger.info("Objects in map:")
        for obj in self.renderer.tmx_data.objects:
            logger.info(obj)
            for k, v in obj.properties.items():
                logger.info("%s\t%s", k, v)

        logger.info("GID (tile) properties:")
        for k, v in self.renderer.tmx_data.tile_properties.items():
            logger.info("%s\t%s", k, v)

        logger.info("Tile colliders:")
        for k, v in self.renderer.tmx_data.get_tile_colliders():
            logger.info("%s\t%s", k, list(v))

    def translate_pos(self, pos):
        (x, y) = pos
        (winx, winy) = self.window
        return (x - winx, y - winy)

    def draw(self, surface) -> None:

        temp = pygame.Surface(size=(640, 480))

        (winx, winy) = self.window

        (px, py) = self.translate_pos(self.player.pos)

        if 640 - px < 20:
            winx = winx + (px - (640 - 20))
        elif px < 20:
            winx = winx - (20 - px)

        if 480 - py < 60:
            winy = winy + (py - (480 - 60))
        elif py < 20:
            winy = winy - (20 - py)

        self.window = (winx, winy)

        # render the map onto the temporary surface
        self.renderer.render_map(temp, self.window)

        # now resize the temporary surface to the size of the display
        # this will also 'blit' the temp surface to the display
        pygame.transform.smoothscale(temp, surface.get_size(), surface)

        surface.blit(self.player.render(), self.translate_pos(self.player.pos))

    def run(self) -> None:
        movement = (0, 0)
        if self.moving:
            for key, (movx, movy) in keys.items():
                if self.keys[key]:
                    (x, y) = movement
                    movement = (x + movx, y + movy)
        self.player.move(movement, get_diff())

        self.draw(self.screen)

    def handle_input(self, events) -> None:

        self.keys = pygame.key.get_pressed()

        self.moving = False
        for k in keys.keys():
            if self.keys[k]:
                self.moving = True
                break
