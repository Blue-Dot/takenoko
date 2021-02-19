import pygame
import config as c
from button import Button

class Hand(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.objectives = []
        self.surface = None
    
    def draw(self, surface):
        if len(self.objectives) > 0:
            width = len(self.objectives) * c.objective_width + (len(self.objectives) - 1) * c.objective_spacing
            rect = pygame.rect.Rect((c.width - width) / 2, c.objective_y, width, c.objective_height)

            for index, i in enumerate(self.objectives):
                i.draw(surface, (rect.x + index * (c.objective_width + c.objective_spacing), rect.y))

    def add_objective(self, objective):
        self.objectives.append(objective)
    
    def remove_objective(self, objective):
        self.objectives.remove(objective)
        self.game.current_player.complete_objective(objective)

class Objective(pygame.sprite.Sprite):
    def __init__(self, hand):
        self.hand = hand

        self.surface = pygame.surface.Surface((c.objective_width, c.objective_height))
        self.surface.fill(c.objective_colour)

        self.button = Button('Place', 0, 0, 70, 30, self.complete)
    
    def draw(self, surface, coords):
        surface.blit(self.surface, coords)

        self.button.move_to(coords[0] + 5, coords[1] + 5)
        self.button.draw(surface)

    def valid(self):
        '''return true if the objective can be completed'''
        return True
    
    def complete(self):
        self.hand.remove_objective(self)

