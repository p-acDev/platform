import pygame
import json
from keys import KEYS

with open("settings.json", "r") as f:
    settings = json.load(f)

with open("world_params.json", "r") as f:
    world_params = json.load(f)

with open("colors.json", "r") as f:
    colors = json.load(f)


class Player(pygame.sprite.Sprite):
    
    def __init__(self, x0, y0):

        pygame.sprite.Sprite.__init__(self)
        # import the setting for the player
        with open("player.json", "r") as f:
            self.player_data = json.load(f)

        # create a pygame image to
        self.image = pygame.Surface((self.player_data["rect_width"],
                                     self.player_data["rect_height"]))
        self.image.fill(colors["GREEN"])
        self.rect = self.image.get_rect()

        # initial position
        self.rect.left = x0
        self.rect.bottom = y0

    def go_left(self, keystate):

        if keystate[KEYS[self.player_data["go_left"]]] and self.rect.left > 0:
            self.rect.x -= self.player_data["speedx"]

        return None

    def go_right(self, keystate):

        if keystate[KEYS[self.player_data["go_right"]]] and self.rect.right < settings["WIDTH"]:
            self.rect.x += self.player_data["speedx"]

        return None

    def jump(self, keystate, events, hits):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == KEYS[self.player_data["jump"]] and hits:
                    self.rect.y -= self.player_data["jumpPower"]

        return None

    def apply_gravity(self):

        if self.rect.bottom < settings["HEIGHT"]:
            self.rect.y += world_params["GRAVITY"]

        return None

    def update(self, events, hits) -> None:

        # get the dictionnary of key that are pressed
        keystate = pygame.key.get_pressed()

        # move the player according to key presseds
        self.go_left(keystate)
        self.go_right(keystate)
        self.jump(keystate, events, hits)
        self.apply_gravity()

        return None


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        # create a pygame image to
        self.image = pygame.Surface((width, height))
        self.image.fill(colors["WHITE"])
        self.rect = self.image.get_rect()

        # initial position
        self.rect.center = (x, y)
