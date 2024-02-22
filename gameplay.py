import pygame, logging

from sprites import Sprites
from tiled import TiledRenderer

from tick import get_diff, get_tick

logger = logging.getLogger(__name__)

map = "gfx/basic.tmx"

keys = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


class Player:
    def __init__(self, sprites, renderer, pos=(120, 120)):
        self.movement_speed = 6  # pps
        self.animation_speed = 300  # ms per frame
        self.last_frame = 0
        self.pos = pos
        self.sprites = sprites
        self.renderer = renderer
        self.lastmovement = (0, 1)
        self.movement = (0, 0)
        self.w = 16
        self.h = 32
        self.boxx = 0
        self.boxy = 16
        self.boxw = 16
        self.boxh = 16

    def is_moving(self) -> bool:
        return self.movement != (0, 0)

    def get_touching_tiles(self, pos) -> list:
        (x, y) = pos
        (x, y) = (int(x / 16), int(y / 16))
        #print(["i think i am trying to move to:", (x, y)])

        points = [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)]
        #print(["i am looking for these tiles: ", points])
        tiles = [
            (_x * 16, _y * 16, self.renderer.tmx_data.layers[0].data[_y][_x])
            for (_x, _y) in points
        ]
        return set(tiles)

    def can_move_to(self, x, y):

        h = self.h
        w = self.w

        me = pygame.Rect((x+self.boxx, y+self.boxy), (self.boxw, self.boxh))
        tiles = self.get_touching_tiles((x, y))
        blockers = self.renderer.blockers

        def uhg(tile, blockers):
            (x, y, gid) = tile
            return [
                pygame.Rect((int(x + b.x), int(y + b.y)), (b.w, b.h)) for b in blockers
            ]

        colliders = filter(
            lambda x: x,
            [
                uhg((x, y, gid), blockers[gid]) if gid in blockers else None
                for (x, y, gid) in tiles
            ],
        )

        for c in colliders:
            print([c, me])
            if me.collidelist(c) > -1:
                return False
        return True

    def move(self, movement, time) -> None:
        secs = time / 100
        self.movement = movement
        if self.is_moving():
            self.lastmovement = movement
        (posx, posy) = self.pos
        (movx, movy) = movement

        if abs(movx) + abs(movy) == 2:
            secs = secs * 0.7

        movx = movx * (self.movement_speed * secs)
        movy = movy * (self.movement_speed * secs)

        if movement != (0, 0) and not self.can_move_to(posx + movx, posy + movy):
            (movx, movy) = (0, 0)

        self.pos = (posx + movx, posy + movy)

    def render(self) -> pygame.Surface:

        sprites = self.sprites.sprites[
            "player." + movement_to_direction(self.lastmovement)
        ]
        frame = (
            0
            if not self.is_moving()
            else int(get_tick() / self.animation_speed) % len(sprites)
        )
        sprite = sprites[frame]

        return sprite


def movement_to_direction(movement) -> str:
    # i hate this but i can't decide on a better way
    # movement should only be a tuple with two values of -1, 0, or 1
    # default to "s"

    dir = ["n", "", "s", "w", "", "e"]
    (x, y) = movement
    return dir[y + 1] + dir[x + 4] or "s"


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

        #print(["winx", (winx, winy), "p", (px, py)])

        if 640 - px < 20:
            self.window = (winx + (px - (640 - 20)), winy)
        elif px < 20:
            self.window = (winx - (20 - px), winy)

        if 480 - py < 60:
            print((winy, py))

            self.window = (winx, winy + (py - (480 - 60)))
        elif py < 20:
            self.window = (winx, winy - (20 - py))

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
