import pygame
from coordinates import Cartesian
from plots import Plot, TempTile, Pond
from rivers import RiverSystem
from coordinates import Axial


class Board(pygame.sprite.Sprite):  # JUST A GENERAL BOARD - could be for plot objective cards(?)
    def __init__(self, size, center):
        super().__init__()
        self.size = size
        self.center = center
        # Keys are in the form (q coordinate, r coordinate)
        self.hash_table = {}

        self.river_system = RiverSystem(self)

        self.hovered_tiles = []  # For highlight_tiles method - tiles hovered in previous frame
        self.clicked_tiles = []

        # A placeholder tile for when placing a new tile (directly under the mouse)
        self.temp_table = {}

    def draw(self, surface):
        for tile in self.hash_table:
            self.hash_table[tile].draw(surface, self.size, self.center)

        self.river_system.draw(surface)

        for tile in self.temp_table:
            self.temp_table[tile].draw(surface, self.size, self.center)

    def place(self, tile):  # Can't use 'add' because that's allready a method of pygame.sprite.Spirte which I am using - so I used 'place' instead
        #coords = (tile.axial.q, tile.axial.r)
        if tile.axial.get_coords() in self.hash_table:
            # Tried to put a tile in a spot which allready had a tile
            raise Exception(
                'hi future max; you tried to put a hexagon in a place on the board which allready had a hexagon there')
            # return False
        self.hash_table[tile.axial.get_coords()] = tile


class MainBoard(Board):  # THE MAIN BOARD WHICH IS FOR EVERYTHING
    def highlight_tiles(self, hash_table):  # TESTED - works!
        '''returns (q, r) coordinates of selected tile. Returns 'mouse_off' when mouse is moved off tile'''
        is_clicked = pygame.mouse.get_pressed()[0]  # Primary button clicked?
        mouse_coords_axial = self.calculate_mouse_coords()

        for tile_coords in self.clicked_tiles:
            # Tile was clicked and someone let go whilst still on the tile!! *ie selected*
            if (not is_clicked) and mouse_coords_axial.coords == tile_coords:
                hash_table[tile_coords].un_hover()
                self.clicked_tiles.remove(tile_coords)
                return tile_coords
            # Tile was clicked, but someone dragged their mouse off.
            elif mouse_coords_axial.coords != tile_coords:
                self.clicked_tiles.remove(tile_coords)
                # self.hovered_tiles.remove(tile_coords)
                hash_table[tile_coords].un_hover()
                return 'mouse_off'

        for tile_coords in self.hovered_tiles:
            if mouse_coords_axial.coords != tile_coords:  # Some one has moved their mouse off the tile
                self.hovered_tiles.remove(tile_coords)
                hash_table[tile_coords].un_hover()
                return 'mouse_off'

        if mouse_coords_axial.get_coords() in hash_table:
            if is_clicked:
                if mouse_coords_axial.coords not in self.clicked_tiles:
                    hash_table[mouse_coords_axial.coords].click()
                    self.clicked_tiles.append(mouse_coords_axial.coords)
            else:
                if mouse_coords_axial.coords not in self.hovered_tiles:
                    hash_table[mouse_coords_axial.coords].hover()
                    self.hovered_tiles.append(mouse_coords_axial.coords)

    def select_tile(self):  # Returns the tile if one is selected
        '''Returns none if no hexagons were selected in that frame, returns the tile object if one was'''
        return_val = self.highlight_tiles(self.hash_table)
        if return_val and return_val != 'mouse_off':
            # if isinstance(self.hash_table[return_val], Plot): #Makes sure the pond can't be returned
            return self.hash_table[return_val]

    def place_tile(self, tile):  # Use the mouse to place a new tile
        mouse_coords_axial = self.calculate_mouse_coords()

        # Add current tile location as a temp tile
        temp_tile = TempTile(mouse_coords_axial.q, mouse_coords_axial.r, self)

        # CHECK TEMP TILE IS VALID:
        # If next to > 1 plot, or next to pond, it is valid
        valid = False
        neighbours = temp_tile.neighbours(self)
        if len(neighbours) > 1:
            valid = True
        for i in neighbours:
            if isinstance(i, Pond):
                valid = True

        # If allready in map, it is not valid
        if mouse_coords_axial.get_coords() in self.hash_table:
            valid = False

        if valid:
            self.temp_table[mouse_coords_axial.get_coords()] = TempTile(
                mouse_coords_axial.q, mouse_coords_axial.r, self)

        try:
            return_val = self.highlight_tiles(self.temp_table)
        # If there is a problem with 'highlight tiles' - typically at edge cases (ie someone clicked on a tile but didnt release etc.)
        except LookupError:
            self.hovered_tiles = []
            self.clicked_tiles = []
            self.temp_table = {}
            return_val = None

        if return_val == 'mouse_off':
            # Mouse moved off tile, so clear temp_table (not temp tiles)
            self.temp_table = {}
        elif return_val:
            # USER CLICKED IN A VALID LOCATION: PLACE TILE
            if tile.improvement:
                plot = Plot(mouse_coords_axial.q, mouse_coords_axial.r,
                            tile.colour, self, tile.improvement)
            else:
                plot = Plot(mouse_coords_axial.q,
                            mouse_coords_axial.r, tile.colour, self)
            self.place(plot)

            # Irrigate the new plot if it is next to a river:
            if self.river_system.is_irrigated(plot):
                plot.irrigate()

            self.hovered_tiles = []
            self.clicked_tiles = []
            self.temp_table = {}

            return True

    def calculate_mouse_coords(self):
        mouse_coords = pygame.mouse.get_pos()
        return Cartesian(mouse_coords[0], mouse_coords[1], self.size, self.center)

    def search_bamboo(self, colour, length, improvement, exclude=None):
        '''returns coords of tile if a bamboo of specific colour, length and improvement is in the board'''
        exclude = [] if exclude is None else exclude  # This is because the default value for exclude can't be []

        for i in self.hash_table:
            if i not in exclude:  # exclude shouldn't be valid
                tile = self.hash_table[i]
                if tile.colour == colour:
                    if tile.bamboo_amount == length:
                        if improvement is not None:  # Ie cares about improvement
                            if improvement == 'None':  # Ie can't have an improvement
                                if tile.improvement is None:
                                    return i
                            else:
                                if tile.improvement == improvement:
                                    return i
                        else:
                            return i
        return False

    def search_plots(self, needle) -> bool:  # thank you freddie
        ''' needle in form of [[[0, 0], "green"], [[0, 1], "pink"], [[1, 0], "pink"]] - must be two or more plots '''

        # base tile = ...
        for i in needle:
            if i[0] == [0, 0]:
                base_tile = i[1]

        if 'base_tile' not in locals():
            raise Exception('plot objective card doesn\'t have a [0, 0] tile')

        # create vector pathway
        path = [PlotVector(
            Axial(needle[1][0][0], needle[1][0][1]), needle[1][1])]

        for i in needle[2:]:
            dest_coords = Axial(i[0][0], i[0][1])
            vector = dest_coords.subtract(path[-1].coords)
            path.append(PlotVector(vector, i[1]))

        poss_base_tiles = []
        for coords in self.hash_table:
            if self.hash_table[coords].colour == base_tile:
                poss_base_tiles.append(coords)

        # works up to this point

        # for correct colour tile in hash table:
        #   rotate vector pathway or something?
        #   tile irrigated?
        #   tile correct colour
        #   end of pathway?
        #       return True
        #   move to next one in pathway

        return True


class PlotVector():
    '''a link between a vector and plot colour - used in MainBoard.search_plots'''

    def __init__(self, coords: Axial, colour: str):
        self.coords = coords
        self.colour = colour

    def rotate(self):  # INCOMPLETE
        pass
