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
        # coords = (tile.axial.q, tile.axial.r)
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

    def select_tile(self) -> Plot:  # Returns the tile if one is selected
        '''Returns none if no hexagons were selected in that frame, returns the tile object if one was'''
        return_val = self.highlight_tiles(self.hash_table)
        if return_val and return_val != 'mouse_off':
            # if isinstance(self.hash_table[return_val], Plot): #Makes sure the pond can't be returned
            return self.hash_table[return_val]
        return None

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

        # create vector pathway
        path = VectorPath()
        for i in needle:
            path.add_vector(i)

        # create a list of all the posisble base tiles
        base_tile_colour = path.base_tile()
        poss_base_tiles = []

        for coords in self.hash_table:
            if self.hash_table[coords].colour == base_tile_colour:
                poss_base_tiles.append(Axial(coords[0], coords[1]))

        # for i in path.path:
        #    print(i['coords'].get_coords())

        # for correct colour tile in hash table:
        for poss_base_tile in poss_base_tiles:
            # print('poss_base_tile %s' % str(poss_base_tile.get_coords()))
            for i in range(6):
                path.rotate()
                if self.test_path(path, poss_base_tile):
                    return True
        return False

    def test_path(self, path, start):  # INCOMPLETE
        pointer_location = start

        for i in path.path:
            pointer_location = pointer_location.sum(i['coords'])

            # print(pointer_location.get_coords())

            if pointer_location.get_coords() in self.hash_table:
                current_tile = self.hash_table[pointer_location.get_coords()]
            else:
                return False

            if current_tile.colour != i['colour']:
                return False
            if not current_tile.is_irrigated:  # can't be pond so this is okay
                return False

        return True


class VectorPath():
    '''an ordered set of vectors describing how to get through the hole pattern - used in MainBoard.search_plots'''

    def __init__(self):
        self.path = []

    def add_vector(self, tile: [[int, int], str]):
        coord_q = tile[0][0]
        coord_r = tile[0][1]
        colour = tile[1]

        if not self.path:  # If list is empty
            self.path.append(
                {'coords': Axial(coord_q, coord_r), 'colour': colour}
            )
        else:
            self.path.append(
                {'coords': Axial(coord_q, coord_r).subtract(self.path[-1]['coords']),
                 'colour': colour}
            )

    def rotate(self):  # INCOMPLETE
        for i in self.path:
            i['coords'] = i['coords'].rotate(self.path[0]['coords'])

    def base_tile(self):
        '''returns the colour of the [0, 0] tile'''
        return self.path[0]['colour']
