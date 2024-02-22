import pygame
import itertools
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

import logging

logger = logging.getLogger(__name__)


class TiledRenderer(object):
    """
    Super simple way to render a tiled map
    """

    def __init__(self, filename):
        tm = load_pygame(filename)

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.map_size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.lasttiles = {}

        self.blockers = self.colliders_to_rects()

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

    def render_map(self, surface, window):

        # fill the background color of our render surface
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        # iterate over all the visible layers, then draw them
        for layer in self.tmx_data.visible_layers:
            # each layer can be handled differently by checking their type

            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(surface, layer, window)

            elif isinstance(layer, TiledObjectGroup):
                self.render_object_layer(surface, layer)

            elif isinstance(layer, TiledImageLayer):
                self.render_image_layer(surface, layer)

    def in_view(self, x, y, window):
        (winx, winy) = window
        return x >= winx and x <= winx + 640 and y >= winy and y <= winy + 480

    def render_tile_layer(self, surface, layer, window):
        """Render all TiledTiles in this layer"""
        # deref these heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit
        in_view = self.in_view
        (winx, winy) = window
        # 40x30

        tiles = []
        start_x = int(winx / 16)
        start_y = int(winy / 16)
        perms = itertools.product(
            range(start_x, start_x + 41), range(start_y, start_y + 31)
        )
        tiles = []
        for i, j in perms:
            if (j < len(layer.data) and i < len(layer.data[j]) and layer.parent.images[layer.data[j][i]]):
                tiles.append((i, j, layer.parent.images[layer.data[j][i]]))

        #tiles = [
        #    (i, j, layer.parent.images[layer.data[j][i]])
        #    for (i, j) in perms
        #    if j < len(layer.data) and i < len(layer.data[j]) and layer.parent.images[layer.data[j][i]]
        #]
                

        # for i in range(t_start_x,t_start_x+40):
        #    for j in range(t_start_y,t_start_y+40):
        #        if layer.parent.images[layer.data[j][i]]:
        #           tiles.append((i, j, layer.parent.images[layer.data[j][i]]))

        # tiles = list(filter(lambda t: in_view(t[0]*tw, t[1]*th, window), layer.tiles())) \
        #        if layer.name not in self.lasttiles \
        #        else self.lasttiles[layer.name]

        for x, y, image in tiles:
            surface_blit(image, (x * tw - winx, y * th - winy))

        self.lasttiles[layer.name] = tiles

    def render_object_layer(self, surface, layer):
        """Render all TiledObjects contained in this layer"""
        # deref these heavily used references for speed
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
