import pygame

fontpath = "gfx/Acme-Regular.ttf"

color = (0,255,0)


class Title:
    def __init__(self, gamerunner, nextrunner, title):
        self.title = title
        self.gamerunner = gamerunner
        self.nextrunner = nextrunner
        self.screen = gamerunner.screen
        self.dirty = True
        self.font = pygame.font.Font(fontpath, 72)


    def run(self):
        if self.dirty:
            ren = self.font.render(self.title, 1, color)
            self.screen.blit(ren, (self.screen.get_width() / 2 - ren.get_width() / 2,self.screen.get_height() / 2 - ren.get_height() / 2))
            self.dirty = False

        

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.gamerunner.runner = self.nextrunner