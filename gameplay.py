import pygame, logging

from sprites import Sprites
from tiled import TiledRenderer

from tick import get_diff, get_tick

logger = logging.getLogger(__name__)

map = "gfx/basic.tmx"

keys = {
    pygame.K_UP: (0,-1),
    pygame.K_DOWN: (0,1),
    pygame.K_LEFT: (-1,0),
    pygame.K_RIGHT: (1,0),
}

class Player:
    def __init__(self, sprites, pos=(10,10)):
        self.movement_speed = 10 # pps
        self.animation_speed = 3 # fps
        self.last_frame = 0
        self.pos = pos
        self.sprites = sprites
        self.lastmovement = (0,1)
        self.movement = (0,0)

    def is_moving(self):
        return self.movement != (0,0)


    def move(self, movement, time):
        secs = time/100
        self.movement = movement
        self.lastmovement = movement
        (posx, posy) =  self.pos
        (movx, movy) = movement

        if abs(movx + movy) == 2:
            secs * .7

        movx = movx * (self.movement_speed * secs)
        movy = movy * (self.movement_speed * secs)

        self.pos = (posx + movx, posy + movy)

    def render(self):

        sprites = self.sprites.sprites["player."+movement_to_direction(self.lastmovement)]
        frame = 0 if not self.is_moving() else int(get_tick() / self.animation_speed) % len(sprites)
        sprite = sprites[frame]

        return sprite



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
        self.ingame = True

        self.player = Player(self.sprites)

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

        surface.blit(self.player.render(), self.player.pos)


    def run(self):
        movement = (0,0)
        if self.moving:
            for key, (movx, movy) in keys.items():
                if self.keys[key]:
                    (x,y) = movement
                    movement = (x + movx, y + movy)
        self.player.move(movement, get_diff())

        self.draw(self.screen)

    def handle_input(self, events):

        self.keys = pygame.key.get_pressed()

        self.moving = False
        for k in keys.keys():
            if self.keys[k]:
                self.moving = True
                break