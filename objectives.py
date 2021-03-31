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
                if i is not None:
                    i.draw(surface, (rect.x + index * (c.objective_width + c.objective_spacing), rect.y))

    def add_objective(self, objective):
        if len(self.objectives) < 5:
            self.objectives.append(objective)
        else:
            return False

    def full(self):
        if len(self.objectives) < 5:
            return False
        return True
    
    def remove_objective(self, objective):
        self.objectives.remove(objective)
        self.game.current_player.complete_objective(objective)

class Objective(pygame.sprite.Sprite):
    def __init__(self, hand, points):
        '''hand = None if not in a hand'''
        self.hand = hand
        self.points = points

        self.button = Button('Place', 0, 0, 70, 30, self.complete)
    
    def create_surface(self):
        self.surface = pygame.surface.Surface((c.objective_width, c.objective_height))
        self.surface.fill(c.objective_colour)

    def draw(self, surface, coords):
        self.update_surface()
        surface.blit(self.surface, coords)

        self.button.move_to(coords[0] + 5, coords[1] + 5)
        self.button.draw(surface)

    def valid(self):
        '''return true if the objective can be completed'''
        return True
    
    def complete(self):
        if self.hand is not None:
            if self.valid():
                self.hand.remove_objective(self)
            else:
                print('Not complete yet!')
        else:
            raise Exception('This objective is not in a hand')

    def assign_hand(self, hand):
        self.hand = hand

    def update_surface(self):
        pass

class Panda(Objective):
    def __init__(self, points, bamboo, hand):
        super().__init__(hand, points)
        self.bamboo = bamboo
    
    def valid(self):
        current_player = self.hand.game.current_player
        if current_player.trade_bamboo(self.bamboo):
            return True
        return False

    def update_surface(self):
        self.create_surface()

        for index, i in enumerate(self.bamboo):
            bamboo_image = pygame.image.load(c.image_bamboo[c.tile_colours.index(i)])
            bamboo_image = pygame.transform.scale(bamboo_image, c.objective_bamboo_dimensions)
            self.surface.blit(bamboo_image, ((c.objective_width - c.objective_bamboo_dimensions[0]) / 2, index * 30 + 50))

class Gardener(Objective):
    def __init__(self, points, bamboo, hand):
        super().__init__(hand, points)
        self.bamboo = bamboo
    
    def valid(self):
        board = self.hand.game.board
        