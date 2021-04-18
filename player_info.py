import pygame
import config as c
from text_object import TextObject
import colours

class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        super().__init__()

        self.player = player
        self.coords = (x, y)

        self.objects = pygame.sprite.Group()

        self.create_objects()
        self.create_surface()

    def create_surface(self):
        self.surface = pygame.surface.Surface(
            (c.player_info_height, c.player_info_width))
        self.surface.fill(c.objective_colour)

    def create_objects(self):
        self.rivers_object = TextObject('Rivers: %i' % (self.player.river_reserve), colours.WHITE, 10, 10, 20)
        self.points_object = TextObject('Points: %i' % (self.player.points), colours.WHITE, 10, 40, 20)
        self.objects.add((self.rivers_object, self.points_object))

    def draw(self, surface):
        self.update()

        surface.blit(self.surface, self.coords)
        self.objects.draw(surface)

    def update(self):
        self.rivers_object.new_text('Rivers %i' % (self.player.river_reserve))
        self.points_object.new_text('Points %i' % (self.player.points))
        
