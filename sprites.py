from spritesheet import spritesheet

sprite_dict = {
    "./gfx/character2.png": {
        "alpha_color": (0, 0, 0, 255),
        "sprites": {
            "player.s": ((0, 0, 16, 32), 4),
            "player.se": ((0, 0, 16, 32), 4),
            "player.sw": ((0, 0, 16, 32), 4),
            "player.n": ((0, 64, 16, 32), 4),
            "player.ne": ((0, 64, 16, 32), 4),
            "player.nw": ((0, 64, 16, 32), 4),
            "player.e": ((0, 32, 16, 32), 4),
            "player.w": ((0, 96, 16, 32), 4),
        },
    }
}


class Sprites:
    def __init__(self):
        self.sprites = {}
        for file, data in sprite_dict.items():
            ss = spritesheet(file)
            for sprite, (rect, count) in data["sprites"].items():
                self.sprites[sprite] = ss.load_strip(rect, count, data["alpha_color"])
