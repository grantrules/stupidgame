import pygame, logging

from sprites import Sprites
from tiled import TiledRenderer

logger = logging.getLogger(__name__)

map = "gfx/basic.tmx"

keys = {
    pygame.K_UP: (0,-1),
    pygame.K_DOWN: (0,1),
    pygame.K_LEFT: (-1,0),
    pygame.K_RIGHT: (1,0),
}

def movement_to_direction(movement):
    # i hate this but i can't decide on a better way
    # movement should only be a tuple with two values of -1, 0, or 1
    # default to "s"
    
    dir = ["n", "", "s",
        "w", "", "e"]
    (x,y) = movement
    return dir[y+1] + dir[x+4] or "s"

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
        self.pos = (0,0)
        self.lastmovement = (0,1)
        self.ingame = True

    def load_map(self, filename):
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

    def draw(self, surface):

        temp = pygame.Surface(size=(640,480))

        # render the map onto the temporary surface
        self.renderer.render_map(temp, (0,0))

        # now resize the temporary surface to the size of the display
        # this will also 'blit' the temp surface to the display
        pygame.transform.smoothscale(temp, surface.get_size(), surface)

        surface.blit(self.sprites.sprites["player."+movement_to_direction(self.lastmovement)][0], self.pos)


        # display a bit of use info on the display

       



    def run(self):
        if self.moving:
            movement = (0,0)
            for key, (x2, y2) in keys.items():
                if self.keys[key]:
                    (x,y) = movement
                    movement = (x + x2, y + y2)

            self.movement = movement
            self.lastmovement = movement
            (posx, posy) =  self.pos
            (movx, movy) = movement
            self.pos = (posx + movx, posy + movy)
            print(movement, self.pos)
        else:
            self.movement = (0,0)

        self.draw(self.screen)


    def handle_input(self, events):

        self.keys = pygame.key.get_pressed()

        self.moving = False
        for k in keys.keys():
            if self.keys[k]:
                self.moving = True
                break