import pygame
from math import sqrt

import config as c
from coordinates import Axial

axial_directions = [Axial(+1, 0), Axial(+1, -1), Axial(0, -1), Axial(-1, 0), Axial(-1, +1), Axial(0, +1)] #This is for 'neighbours' - it is the six directions to go to get each neighbour

class Tile(pygame.sprite.Sprite): #TESTED - works!
    def __init__(self, q, r, image):
        super().__init__()
        self.image = image
        self.axial = Axial(q, r)

        self.tile_height = None
        self.tile_width = None
        self.surface = None

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


class Plot(Tile):
    def __init__(self, q, r, colour, *improvement):
        self.bamboo_amount = 0
        self.bamboo_surface = pygame.surface.Surface((c.bamboo_width, c.bamboo_height * c.max_bamboo))

        self.colour = colour
        self.is_irrigated = True #INCOMPLETE - This should be false in the final game...

        self.colour_index = c.tile_colours.index(colour)
        self.image = c.image_tiles[self.colour_index]

        self.bamboo_image = pygame.image.load(c.image_bamboo[self.colour_index])
        self.bamboo_image = pygame.transform.scale(self.bamboo_image, (c.bamboo_width, c.bamboo_height))

        super().__init__(q, r, self.image)

        if improvement:
            self.improvement = improvement

    def draw(self, surface, size, center):
        self.create_surface(size)
        self.create_bamboo_surface()

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

    def add_bamboo(self, amount):
        if self.bamboo_amount + amount <= 4:
            self.bamboo_amount += amount
            return self.bamboo_amount

    def grow(self, board):
        if self.is_irrigated:
            self.add_bamboo(1)
        
        #Grow the neighbours of the same colour:
        for i in self.neighbours(board):
            if i.colour == self.colour and i.is_irrigated:
                i.add_bamboo(1)

    def remove_bamboo(self, amount):
        if self.bamboo_amount - amount >= 0:
            self.bamboo_amount -= amount
            return self.bamboo_amount

    def eat(self):
        self.remove_bamboo(1)

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

    # -- MOUSE HANDELING --
    def un_hover(self):
        self.image = c.image_tiles[self.colour_index]

    def hover(self):
        self.image = c.image_tiles_hover[self.colour_index]

    def click(self):
        self.image = c.image_tiles_click[self.colour_index]


class Pond(Tile):
    def __init__(self, q, r):
        super().__init__(q, r, c.image_tile_pond)
        self.colour = 'blue' #This is for the neighbour check for the gardener move - so that it is a different colour to any other tile

    def hover(self):
        pass

    def un_hover(self):
        pass

    def click(self):
        pass
