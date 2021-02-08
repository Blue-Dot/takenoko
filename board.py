import pygame
from coordinates import Cartesian
from plots import Plot
from rivers import RiverSystem

class Board(pygame.sprite.Sprite): #JUST A GENERAL BOARD - could be for plot objective cards(?)

    def __init__(self, size, center):
        super().__init__()
        self.size = size
        self.center = center
        self.hash_table = {} #Keys are in the form (q coordinate, r coordinate)

        self.river_system = RiverSystem(size, center)

        self.hovered_tiles = [] # For highlight_tiles method - tiles hovered in previous frame
        self.clicked_tiles = []
    
    def draw(self, surface):
        for tile in self.hash_table:
            self.hash_table[tile].draw(surface, self.size, self.center)

        self.river_system.draw(surface)

    def place(self, tile): #Can't use 'add' because that's allready a method of pygame.sprite.Spirte which I am using - so I used 'place' instead
        coords = (tile.axial.q, tile.axial.r)
        if coords in self.hash_table:
            raise Exception('hi future max; you tried to put a hexagon in a place on the board which allready had a hexagon there')
        self.hash_table[coords] = tile

class MainBoard(Board): #THE MAIN BOARD WHICH IS FOR EVERYTHING

    def highlight_tiles(self): #TESTED - works!
        mouse_coords = pygame.mouse.get_pos()
        is_clicked = pygame.mouse.get_pressed()[0] #Primary button clicked?

        mouse_coords_axial = Cartesian(mouse_coords[0], mouse_coords[1], self.size, self.center)

        for tile_coords in self.clicked_tiles:
            if (not is_clicked) and mouse_coords_axial.coords == tile_coords: # Tile was clicked and someone let go whilst still on the tile!! *ie selected*
                self.hash_table[tile_coords].un_hover()
                self.clicked_tiles.remove(tile_coords)
                return tile_coords
            elif mouse_coords_axial.coords != tile_coords: #Tile was clicked, but someone dragged their mouse off.
                self.clicked_tiles.remove(tile_coords)
                self.hash_table[tile_coords].un_hover()
        
        for tile_coords in self.hovered_tiles:
            if mouse_coords_axial.coords != tile_coords: #Some one has moved their mouse off the tile
                self.hovered_tiles.remove(tile_coords)
                self.hash_table[tile_coords].un_hover()

        if mouse_coords_axial.coords in self.hash_table:
            if is_clicked:
                if mouse_coords_axial.coords not in self.clicked_tiles:
                    self.hash_table[mouse_coords_axial.coords].click()
                    self.clicked_tiles.append(mouse_coords_axial.coords)
            else:
                if mouse_coords_axial.coords not in self.hovered_tiles:
                    self.hash_table[mouse_coords_axial.coords].hover()
                    self.hovered_tiles.append(mouse_coords_axial.coords)
    

    def select_tile(self): # Returns the tile if one is selected
        '''Returns none if no hexagons were selected in that frame, returns the tile object if one was'''
        return_val = self.highlight_tiles()
        if return_val:
            if isinstance(self.hash_table[return_val], Plot): #Makes sure the pond can't be returned
                return self.hash_table[return_val]

        
    def is_line(self, coords_a, coords_b): #INCOMPLETE!!
        if len(coords_a) == 2:
            coords_a.append(0 - coords_a[0] - coords_a[1])
        if len(coords_b) == 2:
            coords_b.append(0 - coords_b[0] - coords_b[1])

        #If one coordinate stays the same, and the other increase by the same absolute amount

