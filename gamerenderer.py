import itertools
import pygame

from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

import logging

logger = logging.getLogger(__name__)


class GameRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, filename, gameplay, window):
        tm = load_pygame(filename)

        self.map_size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.lasttiles = {}
        self.window = window
        self.window_updated = True
        self.gameplay = gameplay

        self.blockers = self.colliders_to_rects()

    def update_window(self):
        
        lastwindow = self.window
        (winx, winy) = self.window

        (px, py) = self.translate_pos(self.gameplay.players[0].pos)

        if 640 - px < 20:
            winx = winx + (px - (640 - 20))
        elif px < 20:
            winx = winx - (20 - px)

        if 480 - py < 60:
            winy = winy + (py - (480 - 60))
        elif py < 20:
            winy = winy - (20 - py)

        self.window = (winx, winy)
        self.window_updated = self.window != lastwindow

    def colliders_to_rects(self):
        # should be 4 points
        # using point a and c should make rect
        # points seem to go counterclockwise
        blockers = {}

        def points_to_rect(points):
            return pygame.Rect((points.x, points.y), (points.width, points.height))

        for k, v in self.tmx_data.get_tile_colliders():
            blockers[k] = [points_to_rect(points) for points in v]

        return blockers

    def render_things(self, surface, layer, isForeground):
        self.render_tile_layer(surface, layer)


    def get_tile_from_layers(self, x, y):
        data = [layer.data[y][x] for layer in self.tmx_data.layers if isinstance(layer, TiledTileLayer)]
        return data

    def render_map(self, surface):

        # fill the background color of our render surface
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        # iterate over all the visible layers, then draw them
        for layer in self.tmx_data.visible_layers:
            # each layer can be handled differently by checking their type

            if isinstance(layer, TiledTileLayer):

                if layer.name == 'things':
                    self.render_things(surface, layer, False)
                    for player in self.gameplay.players:
                        surface.blit(player.render(), self.translate_pos(player.pos))
                else:
                    self.render_tile_layer(surface, layer)

        self.window_updated = False

    def in_view(self, x, y, window):
        (winx, winy) = window
        return x >= winx and x <= winx + 640 and y >= winy and y <= winy + 480

    def render_tile_layer(self, surface, layer):
        """Render all TiledTiles in this layer"""
        # deref these heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit
        (winx, winy) = self.window
        # 40x30

        tiles = []
        start_x = int(winx / 16)
        start_y = int(winy / 16)
        tiles = []

        for i in range(start_x, start_x + 41):
            for j in range(start_y, start_y + 31):
                if (j < len(layer.data) and i < len(layer.data[j]) and layer.parent.images[layer.data[j][i]]):
                    tiles.append((i, j, layer.parent.images[layer.data[j][i]]))

        for x, y, image in tiles:
            surface_blit(image, (x * tw - winx, y * th - winy))

        self.lasttiles[layer.name] = tiles

    def render_object_layer(self, surface, layer):
        """Render all TiledObjects contained in this layer"""
        draw_lines = pygame.draw.lines
        surface_blit = surface.blit

        # these colors are used to draw vector shapes,
        # like polygon and box shapes
        rect_color = (255, 0, 0)

        # iterate over all the objects in the layer
        # These may be Tiled shapes like circles or polygons, GID objects, or Tiled Objects
        for obj in layer:
            # logger.info(obj)

            # objects with points are polygons or lines
            if obj.image:
                # some objects have an image; Tiled calls them "GID Objects"
                surface_blit(obj.image, (obj.x, obj.y))

            else:
                # use `apply_transformations` to get the points after rotation
                draw_lines(
                    surface, rect_color, obj.closed, obj.apply_transformations(), 3
                )

    def render_image_layer(self, surface, layer):
        if layer.image:
            surface.blit(layer.image)


    def translate_pos(self, pos):
        (x, y) = pos
        (winx, winy) = self.window
        return (x - winx, y - winy)