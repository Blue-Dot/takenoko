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

    def create_sides(self):
        for i in range(7):
            surface = pygame.image.load(c.weather_images[i])
            surface = pygame.transform.scale(
                surface, (c.weather_size, c.weather_size))
            self.surfaces.append(surface)

    def draw(self, surface):
        surface.blit(self.surfaces[self.side], (c.weather_x, c.weather_y))

    def roll(self) -> int:
        '''rolls the dice, returns: Sun, 1 = Rain, 2 = Wind, 3 = Storm, 4 = Clouds, 5 = Choice'''
        self.side = random.randint(0, 5)
        return self.side
