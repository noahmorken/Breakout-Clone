import sys

import pygame

from rain_settings import Settings
from rain import Rain
from random import randint

class Raindrop:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # These lines are for fullscreen.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # These lines are for windowed.
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Raindrop")

        self.rain = pygame.sprite.Group()

        self._create_storm()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_rain()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_q:
            sys.exit()

    def _create_storm(self):
        """Create the storm of rain."""
        # Make a raindrop.
        raindrop = Rain(self)
        rain_width, rain_height = raindrop.rect.size
        available_space_x = self.settings.screen_width - (2 * rain_width)
        number_rain_x = available_space_x // (2 * rain_width)

        # Determine the number of rows of rain that fit on the screen.
        available_space_y = (self.settings.screen_height -
                                (3 * rain_height))
        number_rows = available_space_y // (2 * rain_height)
        # print(number_rows)
        
        # Create the full grid of raindrops.
        for row_number in range(number_rows):
            for rain_number in range(number_rain_x):
                self._create_drop(rain_number, row_number)
    
    def _create_drop(self, rain_number, row_number):
        # Create a raindrop and place it in the row.
        raindrop = Rain(self)
        rain_width, rain_height = raindrop.rect.size
        raindrop.x = rain_width + 2 * rain_width * rain_number
        raindrop.rect.x = raindrop.x + randint(-30, 30)
        raindrop.rect.y = raindrop.rect.height + 2 * raindrop.rect.height * row_number + randint(-30, 30)
        self.rain.add(raindrop)

    def _update_rain(self):
        """
        Check if the drop is at the bottom,
          then update the positions of all raindrops in the storm.
        """
        self.rain.update()
        self._check_rain_position()

    def _check_rain_position(self):
        """Respond appropriately if any raindrops have reached the bottom."""
        for raindrop in self.rain.sprites():
            if raindrop.check_bottom():
                removed_raindrops = self._remove_raindrop()
                self._add_raindrop(removed_raindrops)
                break

    def _remove_raindrop(self):
        """Deletes the raindrops when they hit the bottom of the screen."""
        removed_raindrops = 0
        for raindrop in self.rain.copy():
            if raindrop.rect.top >= self.settings.screen_height:
                removed_raindrops += 1
                self.rain.remove(raindrop)
        return(removed_raindrops)

    def _add_raindrop(self, removed_raindrops):
        """Adds another row of raindrops at the top of the screen."""
        for raindrop in range(removed_raindrops):
            raindrop = Rain(self)
            rain_width, rain_height = raindrop.rect.size
            raindrop.rect.x = randint(rain_width, self.settings.screen_width - rain_width)
            raindrop.rect.y = rain_height
            self.rain.add(raindrop)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.rain.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    rd = Raindrop()
    rd.run_game()