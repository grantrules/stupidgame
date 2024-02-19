import pygame

from fonts import fonts

inactive = (255,255,255)
active = (255,0,0)

class GameMenuDialog:
    def __init__(self, question: str, on_yes=None, on_no=None):
        self.question = question
        self.dirty = True
        self.font = fonts["menu"]
        self.selected = 0
        self.lastkeys = []
        self.on_yes = on_yes
        self.on_no = on_no
        self.visible = False

    def draw(self, screen):
        if self.dirty:
            #self.screen.fill((0,0,0))
            ren = self.font.render(self.question, 1, inactive)
            screen.blit(ren, (screen.get_width() /2 - ren.get_width() / 2, 40))

            yes = self.font.render("Yes", 1, active if self.selected == 0 else inactive)
            no = self.font.render("No", 1, active if self.selected == 1 else inactive)

            answidth = yes.get_width() + no.get_width() + 10

            screen.blit(yes, (screen.get_width() / 2 - answidth / 2, 60))
            screen.blit(no, (screen.get_width() / 2 + answidth / 2, 60))

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
                        if self.on_yes:
                            self.on_yes()
                    else:
                        if self.on_no:
                            self.on_no()
                    self.visible = False