import pygame

fontpath = "gfx/Acme-Regular.ttf"

inactive = (255,255,255)
active = (255,0,0)

class GameQuit:
    def __init__(self, gamerunner, lastrunner):
        self.screen = gamerunner.screen
        self.gamerunner = gamerunner
        self.lastrunner = lastrunner
        self.dirty = True
        self.font = pygame.font.Font(fontpath, 20)
        self.selected = 0
        self.lastkeys = []

    def run(self):
        if self.dirty:
            self.screen.fill((0,0,0))
            ren = self.font.render("Are you sure you want to quit?", 1, inactive)
            self.screen.blit(ren, (self.screen.get_width() /2 - ren.get_width() / 2, 40))

            yes = self.font.render("Yes", 1, active if self.selected == 0 else inactive)
            no = self.font.render("No", 1, active if self.selected == 1 else inactive)

            answidth = yes.get_width() + no.get_width() + 10

            self.screen.blit(yes, (self.screen.get_width() / 2 - answidth / 2, 60))
            self.screen.blit(no, (self.screen.get_width() / 2 + answidth / 2, 60))

            self.dirty = False

    def handle_input(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % 2
                    self.dirty = True
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % 2
                    self.dirty = True
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        self.gamerunner.runner = self.lastrunner