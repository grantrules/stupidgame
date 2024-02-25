import pygame

keys = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}




def movement_to_direction(movement) -> str:
    # i hate this but i can't decide on a better way
    # movement should only be a tuple with two values of -1, 0, or 1
    # default to "s"

    dir = ["n", "", "s", "w", "", "e"]
    (x, y) = movement
    return dir[y + 1] + dir[x + 4] or "s"

