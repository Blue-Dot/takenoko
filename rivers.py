import pygame
from coordinates import *
import colours
import config as c
import math

class River(pygame.sprite.Sprite):
    def __init__(self, a, b):
        super().__init__()
        
        #The two ends of the river:
        self.a = a
        self.b = b

    def draw(self, surface, size, center):
        cart_a = self.a.cartesian(size, center)
        cart_b = self.b.cartesian(size, center)
        pygame.draw.line(surface, c.river_colour, cart_a, cart_b, c.river_width)
        print(cart_a, cart_b)

class RiverSystem():
    def __init__(self, size, center):
        self.rivers = []
        self.valid_nodes = []
        self.temp_river = None # A placeholder river when the player is selecting a place to put a river (doesn't count towards irrigation)

        self.size, self.center = size, center

        self.mouse_down = False
    
    def draw(self, surface):
        for river in self.rivers:
            river.draw(surface, self.size, self.center)
        
        if self.temp_river:
            self.temp_river.draw(surface, self.size, self.center)
        
    def add_river(self, a, b):
        self.rivers[(a, b)] = River(a, b)

    def place_river(self): #INCOMPLETE
        '''Use the mouse to place a new river'''
        mouse_coords = pygame.mouse.get_pos()

        mouse_coords_axial = Cartesian(mouse_coords[0], mouse_coords[1], self.size, self.center)
        mouse_coords_cubic = Cubic(mouse_coords_axial.q, mouse_coords_axial.s, mouse_coords_axial.r)
        tile_center = mouse_coords_axial.cartesian(self.size, self.center)
        mouse_offset = (mouse_coords[0] - tile_center[0], mouse_coords[1] - tile_center[1])
        
        if mouse_offset[0] != 0: #Prevents 'division by zero error'
            angle = math.atan(mouse_offset[1] / mouse_offset[0]) * (180 / math.pi) #Angle in degrees
        else:
            angle = math.copysign(90, mouse_offset[1]) #Returns 90 degrees with the correct sign

        if mouse_offset[0] > 0:  #Right hand side of hexagon
            if angle > 30:
                from_centre = ((1, 0, 1), (0, 0, 1)) #The vector form of each end of the river, from the centre of the hexagon
            elif angle > -30:
                from_centre = ((1, 0, 0), (1, 0, 1))
            else: #Angle < -30
                from_centre = ((1, 1, 0), (1, 0, 0))
        else: #Left hand side of hexagon
            if angle > 30:
                from_centre = ((1, 1, 0), (0, 1, 0))
            elif angle > -30:
                from_centre = ((0, 1, 0), (0, 1, 1))
            else: #Angle < -30
                from_centre = ((0, 1, 1), (0, 0, 1))

        a_cubic = Cubic(from_centre[0][0], from_centre[0][1], from_centre[0][2]).sum(mouse_coords_cubic)
        b_cubic = Cubic(from_centre[1][0], from_centre[1][1], from_centre[1][2]).sum(mouse_coords_cubic)

        self.temp_river = River(a_cubic, b_cubic)

        if pygame.mouse.get_pressed()[0]: #If mouse is selected
            self.mouse_down = True
        if (not pygame.mouse.get_pressed()[0]) and self.mouse_down: #Mouse has just been released
            self.rivers.append(self.temp_river)
            self.temp_river = None
            self.mouse_down = False
    
    def adjacent_river(self, tile): #INCOMPLETE
        '''return True if there is adjacent river to the tile, else return False'''
        return True

