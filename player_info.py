import pygame
import config as c
from text_object import TextObject
import colours
from collections import Counter


class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        super().__init__()

        self.player = player
        self.coords = (x, y)

        self.objects = pygame.sprite.Group()

        self.create_surface()
        self.create_objects()

    def create_surface(self):
        self.surface = pygame.surface.Surface(
            (c.player_info_width, c.player_info_height))
        self.surface.fill(c.objective_colour)

    def create_objects(self):
        self.rivers_object = TextObject('', colours.WHITE, 10, 10, 20)
        self.points_object = TextObject(
            '', colours.WHITE, c.player_info_width // 2, 10, 20)
        self.bamboo_label = TextObject('Bamboo:', colours.WHITE, 10, 50, 20)
        self.bamboo_object = TextObject('', colours.WHITE, 10, 80, 20)
        self.improvements_label = TextObject(
            'Improvements:', colours.WHITE, 10, 120, 20)
        self.improvements_object = TextObject('', colours.WHITE, 10, 150, 20)
        self.objects.add((self.rivers_object, self.points_object,
                         self.bamboo_label, self.improvements_label, self.bamboo_object, self.improvements_object))

        self.update()

    def draw(self, surface):
        self.update()
        # self.create_surface()
        self.objects.draw(self.surface)
        surface.blit(self.surface, self.coords)

    def update(self):
        self.rivers_object.new_text('Rivers: %i' % (self.player.river_reserve))
        self.points_object.new_text('Points: %i' % (self.player.points))

        bamboo = Counter(self.player.bamboo_reserve)
        self.bamboo_object.new_text('Green: %i • Yellow: %i • Pink: %i' % (
            bamboo['green'], bamboo['yellow'], bamboo['pink']))

        self.improvements_object.new_text('Irrigation: %i • Panda: %i • Growth: %i' % (
            self.player.improvement_reserve[0], self.player.improvement_reserve[1], self.player.improvement_reserve[2]))

        if self.player.turn:
            self.surface.fill(colours.DARKSLATEBLUE)
        else:
            self.surface.fill(c.objective_colour)
