import pygame
import config as c
import random


class WeatherDice(pygame.sprite.Sprite):
    def __init__(self):
        ''' 0 = Sun, 1 = Rain, 2 = Wind, 3 = Storm, 4 = Clouds, 5 = Choice, 6 = None '''

        super().__init__()

        self.surfaces = []
        self.create_sides()
        self.side = 6

        self.start_time = -1  # time in ms when roll started
        self.rolls = 0

    def create_sides(self):
        for i in range(7):
            surface = pygame.image.load(c.weather_images[i]).convert_alpha()
            surface = pygame.transform.scale(
                surface, (c.weather_size, c.weather_size))
            self.surfaces.append(surface)

    def draw(self, surface):
        surface.blit(self.surfaces[self.side], (c.weather_x, c.weather_y))

    def roll(self) -> int:
        '''rolls the dice, returns: Sun, 1 = Rain, 2 = Wind, 3 = Storm, 4 = Clouds, 5 = Choice'''
        self.side = random.randint(0, 5)
        return self.side

    def throw(self):
        '''rolls the dice 5 times, and returns side when finished'''
        if self.start_time == -1:
            # first call of 'throw'
            self.start_time = pygame.time.get_ticks()
            self.rolls = 0

        print((pygame.time.get_ticks() - self.start_time))

        if (pygame.time.get_ticks() - self.start_time) // 200 > self.rolls:
            self.rolls += 1
            self.roll()

        if self.rolls > 5:
            # finished rolling
            self.start_time = -1
            return self.side
