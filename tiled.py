import pygame
from pytmx import TiledImageLayer
from pytmx import TiledObjectGroup
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

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

    def render_map(self, surface, window):
        """Render our map to a pygame surface

        Feel free to use this as a starting point for your pygame app.
        This method expects that the surface passed is the same pixel
        size as the map.

        Scrolling is a often requested feature, but pytmx is a map
        loader, not a renderer!  If you'd like to have a scrolling map
        renderer, please see my pyscroll project.
        """

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
        return x >= window[0] and x <= window[0] + 640 and y>= window[1] and y <= window[1] + 480


    def render_tile_layer(self, surface, layer, window):
        """Render all TiledTiles in this layer"""
        # deref these heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit

        # iterate over the tiles in the layer, and blit them
        if self.tmx_data.orientation == "orthogonal":
            for x, y, image in layer.tiles():
                if self.in_view(x*tw, y*th, window):
                    surface_blit(image, (x * tw, y * th))

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
            #logger.info(obj)

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
