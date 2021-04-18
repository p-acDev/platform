import json
import pygame
from game_sprites import Player, Platform

# import settings for windows
with open("settings.json", "r") as f:
    settings = json.load(f)

# import the color
with open("colors.json", "r") as f:
    colors = json.load(f)


class Game:

    def __init__(self):
        # initialize pygame and create window
        pygame.init()
        self.screen = pygame.display.set_mode((settings["WIDTH"], settings["HEIGHT"]))
        pygame.display.set_caption(settings["TITLE"])
        self.clock = pygame.time.Clock()

        # to handle the running programe while loop. It handle also the playing loop
        self.running = True

        # handle the playing loop
        # Indeed you can run the program but without playing
        self.playing = True

        # initiate the instances
        self.player = None
        self.all_sprites = None
        self.platforms = None
        self.all_events = None
        self.hits = None

    def new(self):
        # to store all the sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        # create the platforms
        # main floor
        p_floor = Platform(settings["WIDTH"]/2, settings["HEIGHT"] - 20/2, settings["WIDTH"], 20)
        p1 = Platform(settings["WIDTH"]/2, settings["HEIGHT"] - 200/2, 100, 20)
        self.platforms.add(p_floor)
        self.platforms.add(p1)
        self.all_sprites.add(p_floor)
        self.all_sprites.add(p1)

        # create a player and add it to sprite group
        self.player = Player(300, p_floor.rect.top - 100)
        self.all_sprites.add(self.player)
        self.main_loop()

    def main_loop(self):

        while self.playing:
            # set the FPS
            self.clock.tick(settings["FPS"])
            self.events()
            self.update()
            self.draw()

    def update(self):

        # update all sprite in the sprites group
        # update position for instance
        self.all_sprites.update(self.all_events, self.hits)

        # check collision between player and platforms
        self.hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if self.hits:
            self.player.rect.bottom = self.hits[0].rect.top

    def events(self):

        # stop the while loop if user quit
        self.all_events = pygame.event.get()
        for event in self.all_events:
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):

        # draw/render
        self.screen.fill(colors["BLACK"])
        # draw all sprite in the group
        self.all_sprites.draw(self.screen)
        # after drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        # show game over
        pass


if __name__ == "__main__":

    game = Game()
    game.show_start_screen()
    while game.running:
        game.new()
        game.show_go_screen()

    pygame.quit()
