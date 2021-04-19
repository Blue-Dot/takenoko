import pygame
import json

# My imports
import config as c
from player import Player
from text_object import TextObject
from button import Button
from plots import Pond, Plot
from board import MainBoard
from characters import Panda, Gardener
#from objectives import Objective
from piles import Pile
from weather import WeatherDice
from choose_menu import ChooseMenu, MenuItem
from player_info import PlayerInfo


class Game:
    def __init__(self, width, height):

        # -- GENERAL GAME SETUP --

        self.width, self.height = width, height

        pygame.init()
        pygame.font.init()

        self.surface = pygame.display.set_mode((width, height))

        self.background_image = self.tile_background(
            pygame.image.load(c.background_image).convert()
        )  # Generate background image by tiling pattern
        self.frame_rate = c.frame_rate
        self.objects = pygame.sprite.Group()  # All game objects
        self.is_game_running = True
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(c.caption)

        # -- SPEFICIC TAKENOKO SETUP --

        self.game_state = ''  # CURRENT GAME STATE(!!)

        self.players = [Player(self), Player(self)]
        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]
        self.current_player.start_turn()

        # -- GAME OBJECTS --

        self.player_label = None
        self.player_info = []

        self.pile_tiles = None
        self.pile_objectives = {}

        self.menu = None

        self.panda = None
        self.board = None
        self.gardener = None

        self.create_game_objects()

    def tile_background(self, tile):
        ''' Tile background image and store in a surface '''
        background = pygame.Surface((self.width, self.height))
        # This is ceiling division, just without importing 'math'
        for h in range(self.width + tile.get_width() - 1 // tile.get_width()):
            for w in range(self.height + tile.get_height() - 1 // tile.get_height()):
                # Blit the tile onto the correct spot
                background.blit(
                    tile, (w * tile.get_width(), h * tile.get_height()))
        pygame.draw.rect(
            background,
            c.top_bar_colour,
            pygame.Rect(0, 0, self.width, c.top_bar_height),
        )
        pygame.draw.rect(
            background,
            c.top_bar_outline_colour,
            pygame.Rect(0, c.top_bar_height, self.width,
                        c.top_bar_outline_thickness),
        )
        return background

    def draw(self):
        for spr in self.objects.sprites():
            spr.draw(self.surface)

        self.current_player.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_running = False

    # -- OBJECT CREATION --

    def create_game_objects(self):
        self.create_labels()
        self.create_buttons()
        self.create_board()
        self.create_characters()
        self.create_weather()
        self.create_piles()
        self.create_player_info()

    def create_labels(self):
        self.player_label = TextObject(
            'Player: 1',
            c.player_label_colour,
            10,
            (c.top_bar_height - c.font_size) / 2,
            c.font_size,
        )  # Create text at top of screen saying 'player 1'
        self.player_label.add(self.objects)

    def create_buttons(self):
        self.quit_button = Button('quit', c.width - 55, 5, 50, 30, self.b_quit)
        self.quit_button.add(self.objects)

        self.add_objective_button = Button(
            'add objective', 20, 65, 150, 30, self.b_add_objective
        )
        self.add_objective_button.add(self.objects)

        self.grow_button = Button('grow', 20, 65 + 50, 50, 30, self.b_grow)
        self.grow_button.add(self.objects)

        self.next_turn_button = Button(
            'next turn', 20, 165, 90, 30, self.next_turn)
        self.next_turn_button.add(self.objects)

        self.panda_move_button = Button(
            'move panda', 20, 165 + 50, 120, 30, self.b_panda_move
        )
        self.panda_move_button.add(self.objects)

        self.gardener_move_button = Button(
            'move gardener', 20, 265, 150, 30, self.b_gardener_move
        )
        self.gardener_move_button.add(self.objects)

        self.place_river_button = Button(
            'place rivers', 20, 265 + 50, 130, 30, self.b_place_river
        )
        self.place_river_button.add(self.objects)

        self.place_tile_button = Button(
            'place tile', 20, 365, 110, 30, self.b_place_tile
        )
        self.place_tile_button.add(self.objects)

        self.check_bamboo_button = Button(
            'check bamboo', 20, 365 + 50, 150, 30, self.b_check_bamboo
        )
        self.check_bamboo_button.add(self.objects)

        self.roll_dice_button = Button(
            'roll die', 20, 465, 80, 30, self.b_roll_dice)
        self.roll_dice_button.add(self.objects)

        self.open_menu_button = Button(
            'open menu', 20, 465 + 50, 110, 30, self.b_open_menu)
        self.open_menu_button.add(self.objects)

        self.add_river_button = Button(
            'add river', 20, 565, 120, 30, self.b_add_river)
        self.add_river_button.add(self.objects)

    def create_board(self):
        self.board = MainBoard(c.hexagon_size, c.board_center)
        self.board.place(Pond(0, 0, self.board))
        self.board.add(self.objects)

    def create_characters(self):
        self.panda = Panda(c.hexagon_size, c.board_center)
        self.gardener = Gardener(c.hexagon_size, c.board_center)
        self.panda.add(self.objects)
        self.gardener.add(self.objects)

    def create_weather(self):
        self.dice = WeatherDice()
        self.dice.add(self.objects)

    def create_piles(self):
        data_file = open('data.json', 'r')
        data = json.load(data_file)
        data_file.close()

        self.pile_tiles = Pile(data['tiles']).shuffle()  # For placing tiles
        self.pile_objectives['panda'] = Pile(
            data['objectives']['panda']).shuffle()
        self.pile_objectives['gardener'] = Pile(
            data['objectives']['gardener']).shuffle()
        self.pile_objectives['plots'] = Pile(
            data['objectives']['plots']).shuffle()  # For the 'plot' objectives

    def create_player_info(self):
        for index, i in enumerate(self.players):
            self.player_info.append(PlayerInfo(
                i, c.width - c.player_info_width - 20, (index * (c.player_info_height + 20)) + 60))
            self.player_info[-1].add(self.objects)

    # -- BUTTON PRESSED --

    def b_quit(self):
        self.is_game_running = False

    def b_add_objective(self):
        self.game_state = 'add objective'

    def b_grow(self):
        self.game_state = 'grow'

    def b_panda_move(self):
        self.game_state = 'move panda'

    def b_gardener_move(self):
        self.game_state = 'move gardener'

    def b_place_river(self):
        self.game_state = 'place river'

    def b_place_tile(self):
        if self.game_state != 'place tile':
            if not self.pile_tiles.empty():
                self.top_tile = self.pile_tiles.take()
                self.game_state = 'place tile'
            else:
                print('no more tiles lol')
        else:
            print('you have to place a tile now')

    def b_check_bamboo(self):
        self.game_state = 'check bamboo'

    def b_roll_dice(self):
        self.game_state = 'throwing dice'

    def b_open_menu(self):
        self.menu = ChooseMenu([MenuItem(pygame.image.load(c.image_tiles[0])), MenuItem(
            pygame.image.load(c.image_tiles[0])), MenuItem(pygame.image.load(c.image_tiles[1]))], 'choose plot', number=2)
        self.menu.add(self.objects)
        self.game_state = 'choose menu'

    def b_add_river(self):
        self.current_player.river_reserve += 1

    # -- GAME RULES --

    def next_turn(self):
        # Increase current_player_number by 1, but cycle it through the total number of players
        self.current_player.finish_turn()

        self.current_player_number = (self.current_player_number + 1) % (
            c.number_of_players
        )
        self.current_player = self.players[self.current_player_number]

        self.player_label.new_text('Player: %s' %
                                   str(self.current_player_number + 1))

        self.current_player.start_turn()

    def run(self):
        # For testing purposes (a sample map):
        self.board.place(Plot(1, 1, 'green', self.board, 'panda'))
        self.board.place(Plot(0, 1, 'green', self.board))
        self.board.place(Plot(-1, 1, 'green', self.board))
        self.board.place(Plot(0, -1, 'yellow', self.board))
        self.board.place(Plot(-1, 0, 'yellow', self.board))
        self.board.place(Plot(1, 0, 'pink', self.board, 'irrigation'))
        self.board.place(Plot(1, -1, 'pink', self.board))

        # self.players[0].hand.add_objective(Objective(self.players[0].hand))
        # self.players[0].hand.add_objective(Objective(self.players[0].hand))

        # self.board.river_system.add_river(Cubic(0, 1, 0), Cubic(1, 1, 0))

        while self.is_game_running:
            # Reset display by rendering the background image
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()

            # print(self.game_state)

            if self.game_state == 'grow':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    selected_tile.add_bamboo(2)
            elif self.game_state == 'add objective':

                # If the pile is not empty
                if not self.pile_objectives['plots'].empty():
                    if self.current_player.hand.full() is False:
                        objective = self.pile_objectives['plots'].take()
                        objective.assign_hand(self.current_player.hand)
                        self.current_player.hand.add_objective(objective)
                    else:
                        print('your hand is full')
                else:
                    print('no more objectives')

                self.game_state = ''

            elif self.game_state == 'move panda':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    if self.panda.move(selected_tile):  # If it was a valid move
                        bamboo = selected_tile.eat()
                        if bamboo is not False:
                            self.current_player.add_bamboo(bamboo)
                        # Reset game state (panda has moved)
                        self.game_state = ''
            elif self.game_state == 'move gardener':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    if self.gardener.move(selected_tile):  # If it was a valid move
                        selected_tile.grow(self.board)
                        # Reset game state (gardener has moved)
                        self.game_state = ''
            elif self.game_state == 'place river':
                self.board.river_system.place_river()
            elif self.game_state == 'place tile':
                placed_tile = self.board.place_tile(self.top_tile)
                if placed_tile:
                    self.game_state = ''
            elif self.game_state == 'check bamboo':
                colour = input('colour:')
                length = int(input('length:'))
                improvement = input('improvement:')
                if improvement == 'null':
                    improvement = None

                print(self.board.search_bamboo(colour, length, improvement))
                self.game_state = ''
            elif self.game_state == 'throwing dice':
                roll = self.dice.roll()
                if roll:
                    self.game_state = ''
            elif self.game_state == 'choose menu':
                update = self.menu.update()
                if update:
                    print(update)
                    self.game_state = ''
                    self.menu.remove(self.objects)
                    self.menu = None  # garbage collector should clean this up and delete the object
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()


Main_Game = Game(c.width, c.height)

Main_Game.run()
