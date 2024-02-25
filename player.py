import itertools
import pygame
from tick import get_tick
from input import movement_to_direction

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
            (_x * 16, _y * 16, self.renderer.get_tile_from_layers(_x,_y))
            for (_x, _y) in points
        ]
        return tiles

    def can_move_to(self, x, y):

        h = self.h
        w = self.w

        me = pygame.Rect((x+self.boxx, y+self.boxy), (self.boxw, self.boxh))
        tiles = self.get_touching_tiles((x, y))
        blockers = self.renderer.blockers

        def make_rects(x, y, blockers):
            return [
                pygame.Rect((int(x + b.x), int(y + b.y)), (b.w, b.h)) for b in blockers
            ]

        for (x, y, gids) in tiles:
            for gid in gids:
                if gid in blockers:
                    if me.collidelist(make_rects(x, y, blockers[gid])) > -1:
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