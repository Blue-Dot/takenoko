import pygame
#import coordinates
import colours
import config as c

class River(pygame.sprite.Sprite):
    def __init__(self, a, b):
        super().__init__()
        
        #The two ends of the river:
        self.a = a
        self.b = b

    def draw(self, surface, size, center):
        cart_a = self.a.cartesian(size, center)
        cart_b = self.b.cartesian(size, center)
        pygame.draw.line(surface, colours.BLUE2, cart_a, cart_b, c.river_width)
        print(cart_a, cart_b)

class RiverSystem():
    def __init__(self):
        self.rivers = {}
        self.valid_nodes = []
        self.temp_river = None # A placeholder river when the player is selecting a place to put a river (doesn't count towards irrigation)
    
    def draw(self, surface, size, center):
        for river in self.rivers:
            self.rivers[river].draw(surface, size, center)
        
    def add_river(self, a, b):
        self.rivers[(a, b)] = River(a, b)

    def place_river(self): #INCOMPLETE
        '''Use the mouse to place a new river'''
        pass
    
    def adjacent_river(self, tile): #INCOMPLETE
        '''return True if there is adjacent river to the tile, else return False'''
        return True

