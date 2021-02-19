import pygame
from math import sqrt

import config as c
from coordinates import Axial

axial_directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)] #This is for 'neighbours' - it is the six directions to go to get each neighbour

class Tile(pygame.sprite.Sprite): #TESTED - works!
    def __init__(self, q, r, colour, board):
        super().__init__()
        self.colour = colour
        self.axial = Axial(q, r)

        self.tile_height = None
        self.tile_width = None
        self.surface = None

        self.colour_index = c.tile_colours.index(colour)
        self.image = c.image_tiles[self.colour_index]

        self.board = board

    def create_surface(self, size):
        self.surface = pygame.image.load(self.image).convert_alpha()
        self.tile_width = round(sqrt(3) * size)
        self.tile_height = round(2 * size)

        self.surface = pygame.transform.scale(self.surface, (self.tile_width, self.tile_height)) #Scale the image appropriately

    def generate_coords(self, size, center):
        cartesian_coords = self.axial.cartesian(size, center) #Get the cartesian coords of the center
        top_left_coords = (cartesian_coords[0] - (self.tile_width / 2), cartesian_coords[1] - ((self.tile_height) / 2)) #Calculate the coords of the top left of the tile
        return top_left_coords

    def draw(self, surface, size, center):
        self.create_surface(size)
        surface.blit(self.surface, self.generate_coords(size, center)) #Blit the smaller image in the correct spot

    # -- MOUSE HANDELING --
    def un_hover(self):
        self.image = c.image_tiles[self.colour_index]

    def hover(self):
        self.image = c.image_tiles_hover[self.colour_index]

    def click(self):
        self.image = c.image_tiles_click[self.colour_index]

    def neighbours(self, board):
        '''returns a list of tile objects - the neighbours of this tile in the board'''
        neighbours_coords = []
        for i in axial_directions:
            neighbours_coords.append(self.axial.sum(i))
        
        neighbours = []
        for j in neighbours_coords:
            if (j.q, j.r) in board.hash_table:
                neighbours.append(board.hash_table[(j.q, j.r)])

        return neighbours

class Plot(Tile):
    def __init__(self, q, r, colour, board, *improvement):
        super().__init__(q, r, colour, board)

        self.is_irrigated = False

        self.bamboo_amount = 0
        self.bamboo_surface = pygame.surface.Surface((c.bamboo_width, c.bamboo_height * c.max_bamboo))

        self.bamboo_image = pygame.image.load(c.image_bamboo[self.colour_index])
        self.bamboo_image = pygame.transform.scale(self.bamboo_image, (c.bamboo_width, c.bamboo_height))

        if improvement:
            self.add_improvement(improvement[0])
        else:
            self.improvement = None
        
        #Check if I am next to a pond:
        neighbours = self.neighbours(self.board) 
        for i in neighbours:
            if isinstance(i, Pond):
                self.irrigate() #Irrigate if next to a pond instance

    def draw(self, surface, size, center):
        self.create_surface(size)
        self.create_bamboo_surface()
        self.draw_improvement_surface()

        surface.blit(self.surface, self.generate_coords(size, center))

    def create_bamboo_surface(self):
        #Clear bamboo surface:
        self.bamboo_surface = pygame.surface.Surface((c.bamboo_width, c.bamboo_height * c.max_bamboo))

        #Add bamboo to self.surface:
        for i in range(self.bamboo_amount):
            #Put the bamboo in the correct place on the surface:
            self.bamboo_surface.blit(self.bamboo_image, (0, self.bamboo_surface.get_height() - ((i + 1) * c.bamboo_height)))

        self.bamboo_surface.set_colorkey((0, 0, 0, 0)) # Makes sure that the transparent pixels aren't blit (there was a hole in the tiles otherwise)

        self.surface.blit(self.bamboo_surface, (c.bamboo_location_x, c.bamboo_location_y))

    def draw_improvement_surface(self):
        if self.improvement != None:
            self.surface.blit(self.improvement_surface, (c.improvement_location_x, c.improvement_location_y))

    def add_improvement(self, improvement):
        '''improvement = 'irrigation', 'panda' or 'gardener/' '''
        self.improvement = improvement
        self.improvement_index = c.improvements.index(self.improvement)
    
        self.improvement_surface = pygame.image.load(c.improvement_images[self.improvement_index])
        self.improvement_surface = pygame.transform.scale(self.improvement_surface, (round(c.improvement_size * sqrt(3)), c.improvement_size * 2))

        if improvement == 'irrigation':
            self.irrigate()

    def add_bamboo(self, amount):
        if self.bamboo_amount + amount <= 4:
            self.bamboo_amount += amount
            return self.bamboo_amount

    def grow(self, board):
        if self.is_irrigated:
            if self.improvement == 'gardener':
                self.add_bamboo(2)
            else:
                self.add_bamboo(1)
        
        #Grow the neighbours of the same colour:
        for i in self.neighbours(board):
            if i.colour == self.colour and i.is_irrigated:
                if i.improvement == 'gardener':
                    i.add_bamboo(2)
                else:
                    i.add_bamboo(1)

    def remove_bamboo(self, amount):
        if self.bamboo_amount - amount >= 0:
            self.bamboo_amount -= amount
            return self.bamboo_amount

    def eat(self):
        if self.improvement != 'panda':
            self.remove_bamboo(1)
        else:
            return False

    def irrigate(self):
        if not self.is_irrigated:
            self.is_irrigated = True
            if self.improvement == 'gardener':
                self.add_bamboo(2)
            else:
                self.add_bamboo(1)

class Pond(Tile):
    def __init__(self, q, r, board):
        super().__init__(q, r, 'blue', board)

    def grow(self, *args):
        pass

    def eat(self, *args):
        pass

    def irrigate(self, *args):
        pass

class TempTile(Tile): #For placeing a new tile
    def __init__(self, q, r, board):
        super().__init__(q, r, 'grey', board)

        #self.board = board
