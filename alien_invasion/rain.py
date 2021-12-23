import pygame
from pygame.sprite import Sprite

class Rain(Sprite):
    """A class to represent a single raindrop in the program."""

    def __init__(self, rd_game):
        """Initialize the raindrop and set its starting position."""
        super().__init__()
        self.screen = rd_game.screen
        self.settings = rd_game.settings

        # Load the raindrop image and set its rect attribute.
        self.image = pygame.image.load('C:/Users/noahm/Documents/python/alien_invasion/images/raindrop.bmp')
        self.rect = self.image.get_rect()

        # Start each new raindrop near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the raindrop's exact vertical position.
        self.y = float(self.rect.y)
    
    def check_bottom(self):
        """Return True if the raindrop is at the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.top >= screen_rect.bottom:
            return True

    def update(self):
        """Move the raindrop down."""
        self.rect.y += self.settings.raindrop_speed