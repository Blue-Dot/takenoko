import pygame
import config as c
from button import Button
from board import Board
from plots import Plot
from plots import Tile

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
        super().__init__()
        self.hand = hand
        self.points = points

        self.surface = None

        self.button = Button('Place', 0, 0, 70, 30, self.complete)
        self.update_surface()
    
    def create_surface(self):
        self.surface = pygame.surface.Surface((c.objective_width, c.objective_height))
        self.surface.fill(c.objective_colour)

    def draw(self, surface, coords):
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
        self.bamboo = bamboo
        super().__init__(hand, points)
    
    def valid(self) -> bool:
        '''check if objective is valid'''
        current_player = self.hand.game.current_player
        if current_player.trade_bamboo(self.bamboo):
            return True
        return False

    def update_surface(self): #This is to add onto the plain surface that is already there (ie add the bamboo)
        self.create_surface()

        for index, i in enumerate(self.bamboo):
            bamboo_image = pygame.image.load(c.image_bamboo[c.tile_colours.index(i)])
            bamboo_image = pygame.transform.scale(bamboo_image, c.objective_bamboo_dimensions)
            self.surface.blit(bamboo_image, ((c.objective_width - c.objective_bamboo_dimensions[0]) / 2, index * 30 + 50))

class Gardener(Objective):
    def __init__(self, points, bamboo, hand):
        self.bamboo = bamboo
        super().__init__(hand, points)
    
    def valid(self) -> bool:
        '''check if objective is valid'''
        board = self.hand.game.board
        exclude = [] #These are the tiles that have allready been checked (ie if the objective has three bamboo, you must have three different tiles, and not just check one tile three times)

        for i in self.bamboo:
            if board.search_bamboo(i[0], i[1], i[2], exclude) is False:
                return False
            exclude.append(board.search_bamboo(i[0], i[1], i[2], exclude))
        return True
    
    def update_surface(self):
        self.create_surface()
        
        board = Board(30, (c.objective_width / 2, c.objective_height / 2))
        for index, i in enumerate(self.bamboo):
            #this governs how the plots are layed out - ie the first tile will be in 0, 0 etc.
            if index == 0:
                q, r = 0, 0
            elif index == 1:
                q, r = 0, 1
            elif index == 2:
                q, r = -1, 1
            elif index == 3:
                q, r = 2, -1
            board.place(Plot(q, r, i[0], board, i[2]))
            board.hash_table[(q, r)].bamboo_amount = i[1]
        board.draw(self.surface)
        
class Plots(Objective):
    def __init__(self, points, pattern, hand):
        self.pattern = pattern
        super().__init__(hand, points)

    def valid(self) -> bool:
        '''check if objective is valid'''
        board = self.hand.game.board
        return board.search_plots(self.pattern)

    def update_surface(self): #not actually update_surface by the way... it is only used in the creation of the surface, but too late to change it :b
        self.create_surface()
        
        board = Board(15, (c.objective_width / 3, c.objective_height / 2))
        for i in self.pattern:
            board.place(Tile(i[0][0], i[0][1], i[1],  board))

        board.draw(self.surface)
