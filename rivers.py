import pygame
from coordinates import Cubic, Cartesian
import config as c
import math
from plots import Pond

class River(pygame.sprite.Sprite):
    def __init__(self, a, b):
        '''a and b are Cubic objects'''
        super().__init__()
        
        #The two ends of the river:
        self.a = a
        self.b = b

    def draw(self, surface, size, center):
        cart_a = self.a.cartesian(size, center)
        cart_b = self.b.cartesian(size, center)
        pygame.draw.line(surface, c.river_colour, cart_a, cart_b, c.river_width)
        #print(cart_a, cart_b)

class RiverSystem():
    def __init__(self, board):
        self.rivers = {}
        self.valid_nodes = [(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.temp_river = None # A placeholder river when the player is selecting a place to put a river (doesn't count towards irrigation)

        self.board, self.size, self.center = board, board.size, board.center

        self.mouse_down = False
    
    def draw(self, surface):
        for river in self.rivers:
            self.rivers[river].draw(surface, self.size, self.center)
        
        if self.temp_river:
            self.temp_river.draw(surface, self.size, self.center)
        
    def add_river(self, a, b):
        self.rivers[(a, b)] = River(a, b)

    def place_river(self): #INCOMPLETE
        '''Use the mouse to place a new river'''

        #CALCULATE THE COORDINATES OF THE RIVER NEAREST TO THE MOUSE

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

        #HANDLE MOUSE CLICKS AND VALIDITY

        valid = self.check_river(self.temp_river)
        if not valid:
            self.temp_river = None #Don't display a temp river if the mouse is not in a valid place

        if pygame.mouse.get_pressed()[0]: #If mouse is selected
            self.mouse_down = True
        if (not pygame.mouse.get_pressed()[0]) and self.mouse_down: #Mouse has just been released
            if valid: #If it is a valid river
                self.rivers[(a_cubic.coords(), b_cubic.coords())] = River(self.temp_river.a, self.temp_river.b) #This is to create a new instance, so that on the line below, this is not affected
                
                #Add both ends of the river to valid nodes
                if self.temp_river.a.coords() not in self.valid_nodes:
                    self.valid_nodes.append(self.temp_river.a.coords())
                if self.temp_river.b.coords() not in self.valid_nodes:
                    self.valid_nodes.append(self.temp_river.b.coords())

            self.temp_river = None
            self.mouse_down = False

            return True
        return False

        '''
        if not self.check_river(self.temp_river): #If it is not a valid river, reset the temp_river
            self.temp_river = None

        if pygame.mouse.get_pressed()[0]: #If mouse is selected
            self.mouse_down = True
        if (not pygame.mouse.get_pressed()[0]) and self.mouse_down: #Mouse has just been released
            self.rivers[(a_cubic.coords(), b_cubic.coords())] = River(self.temp_river.a, self.temp_river.b) #This is to create a new instance, so that on the line below, this is not affected
            self.temp_river = None
            self.mouse_down = False
        '''

    def check_river(self, river):
        '''check to see if a river is valid --> boolean'''
        if (river.a.coords(), river.b.coords()) in self.rivers or (river.b.coords(), river.a.coords()) in self.rivers: #Is the river allready in the system?
            return False

        adjacent_tiles = self.adjacent_tiles(river)
        if adjacent_tiles == []: #If there are no adjacent tiles
            return False
        for i in adjacent_tiles: #If an adjacent tile is a pond (not valid)   
            if isinstance(i, Pond): 
                return False

        if river.a.coords() not in self.valid_nodes:
            if river.b.coords() not in self.valid_nodes:
                return False

        #ELSE
        return True
        

    def adjacent_tiles(self, river): #WORKS! :)
        direction = river.a.difference(river.b).coords() #This is an 'x' 'y' or 'z' direction (depending on which way the river is pointing)

        #Find the end of the river that is closer to the top of the screen
        #print(river.a.cartesian(c.hexagon_size, c.board_center), river.b.cartesian(c.hexagon_size, c.board_center))
        if river.a.cartesian(10, (0, 0))[1] < river.b.cartesian(10, (0, 0))[1]: #compare relative y coordinates for an arbitary board
            top_node = river.a
        else:
            top_node = river.b
        
        #print(direction)
        #print(top_node.coords())

        if direction == (1, 0, 0): #Ie river is in / direction
            adjacent_tile_coords = (top_node.sum(Cubic(-1, 0, -1)).axial(), top_node.sum(Cubic(-1, -1, 0)).axial())
        elif direction == (0, 1, 0): #Ie river is in \ direction
            adjacent_tile_coords = (top_node.sum(Cubic(0, -1, -1)).axial(), top_node.sum(Cubic(-1, -1, 0)).axial())
        elif direction == (0, 0, 1): #Ie river is in | direction
            adjacent_tile_coords = (top_node.sum(Cubic(-1, 0, 0)).axial(), top_node.sum(Cubic(0, -1, 0)).axial())
        else:
            raise Exception("something has gone wrong with 'direction' in adjacent tiles")

        adjacent_tiles = []

        for i in adjacent_tile_coords:
            if i.get_coords() in self.board.hash_table:
                adjacent_tiles.append(self.board.hash_table[i.get_coords()])
        
        return adjacent_tiles

