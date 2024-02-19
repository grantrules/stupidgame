import pygame

import pickle, logging

fontpath = "gfx/Acme-Regular.ttf"

inactive_color = (255,255,255)
active_color = (255,0,0)

logger = logging.getLogger(__name__)


settings_file = "settings.pickle"

settings_desc = {'music_volume': int,
            'sound_volume': int,
            'fullscreen': bool,
            }

settings = {'music_volume': 10,
            'sound_volume': 10,
            'fullscreen': False,
            }

change_handlers = {}


def register_setting_change_handler(setting, func):
    if setting in change_handlers:
        change_handlers[setting].add(func)
    else:
        change_handlers[setting] = [func]

def call_handlers(setting, value):
    handlers = change_handlers[setting] if setting in change_handlers else []
    for h in handlers:
        h(value)

def update_setting(setting, value):
    last = settings[setting]
    if last != value:
        settings[setting] = value
        call_handlers(setting, value)




font = None

def load_settings():
    user_settings = {}
    try:
        file = open(settings_file, "rb")
        user_settings = pickle.load(file)
        file.close()
    except:
        logger.info("Could not load settings")

    for (key, type) in settings_desc.items():
        if key in user_settings and isinstance(user_settings[key], type):
            update_setting(key, user_settings[key])


def save_settings():
    logger.debug(settings)
    file = open(settings_file, "wb")
    pickle.dump(settings, file)
    file.close()

class Checkbox:
    def __init__(self):
        self.width = 20
    
    def render(self, value):
        surface = pygame.Surface((self.width, self.width))
        pygame.draw.rect(surface, (0,255,0), (0,0,10, 10))
        return surface
    
    def handle_input(self, events, value):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return not value


class Slider:
    def __init__(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step
        self.width = 40

    def render(self, value):
        pos = (value - self.min) / (self.max - self.min) * self.width

        surface = pygame.Surface((self.width,10))
        pygame.draw.rect(surface, (255,255,255), (0,0,self.width,2))
        pygame.draw.rect(surface, (0,255,0), (0,0,pos,2))
        pygame.draw.circle(surface, (0,255,0), (pos, 2), 2.5)
        return surface
    
    def handle_input(self, events, value):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return max(self.min, value - self.step)
                elif event.key == pygame.K_RIGHT:
                    return min(self.max, value + self.step)




class SettingItem:
    def __init__(self, name, key=None, value=None, controller=None, special=False):
        self.name = name
        self.key = key
        self.orig_value = value
        self.value = value
        self.special = special
        self.controller = controller
        if controller:
            self.controller.value = value

    def changed(self):
        return self.value != self.orig_value
    
    def render(self, active=False):
        surface = pygame.Surface((400,font.get_height()))
        
        ren = font.render(self.name, 1, active_color if active else inactive_color)
        surface.blit(ren, (0,surface.get_height() / 2 - ren.get_height() / 2))

        if self.controller:
            ctrl = self.controller.render(self.value)
            surface.blit(ctrl, (surface.get_width() - ctrl.get_width(), surface.get_height() / 2 - ctrl.get_height() / 2))
        return surface
    
    def handle_input(self, events):
        self.value = self.controller.handle_input(events, self.value)
        print("changing "+str(self.value))

def get_settings_menu():
    settings_menu = [
        SettingItem("Sound Effects level", "sound_volume", settings['sound_volume'], Slider(0,10,1)),
        SettingItem("Music level", "music_volume", settings['music_volume'], Slider(0,10,1)),
        SettingItem("Fullscreen", "fullscreen", settings['fullscreen'], Checkbox()),

        SettingItem("Save", "save", special=True)
    ]
    return settings_menu

class GameSettings:
    def __init__(self, gamerunner, lastrunner):
        global font

        self.screen = gamerunner.screen
        self.screen.fill((0,0,0))
        self.gamerunner = gamerunner
        self.lastrunner = lastrunner
        self.dirty = True
        self.font = pygame.font.Font(fontpath, 40)
        font = self.font
        self.selected = 0
        self.menu = get_settings_menu()

    def has_changed(self):
        return any([item.changed() for item in self.menu])
    
    def run(self):
        if self.dirty:
            self.screen.fill((0,0,0))
            for x, item in enumerate(self.menu):
                ren = item.render(active=self.selected == x)
                self.screen.blit(ren, (self.screen.get_width() / 2 - ren.get_width() / 2,x*ren.get_height()+10))
            self.dirty = False

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.menu)
                    self.dirty = True
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.menu)
                    self.dirty = True
                elif event.key == pygame.K_ESCAPE:
                    if self.has_changed():
                        logger.info("prompt to confirm saving")
                        # confirm saving
                        pass
                    else:
                        self.gamerunner.runner = self.lastrunner
                elif event.key == pygame.K_RETURN and self.menu[self.selected].key == "save":
                    logger.info("saving settings")
                    for item in self.menu:
                        if item.key in settings:
                            update_setting(item.key, item.value)
                    save_settings()
                    self.menu = get_settings_menu()
                else:                        
                    self.menu[self.selected].handle_input(events)
                    self.dirty = True
