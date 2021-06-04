import json
import pygame

# My imports
import config as c
from player import Player
from text_object import TextObject
from button import Button, ButtonSystem
from plots import Pond, Plot
from board import MainBoard, Board
from characters import Panda, Gardener
# from objectives import Objective
from piles import Pile
from weather import WeatherDice
from choose_menu import ChooseMenu, MenuItem
from player_info import PlayerInfo


class Game:
    def __init__(self, width, height):

        # -- GENERAL GAME SETUP --

        self.width, self.height = width, height

        pygame.font.init()
        pygame.init()

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

        self.game_state = ''  # CURRENT GAME STATE(!!)\
        self.turn_list = []
        self.turns = 0

        self.weather = 6  # Non existant weather

        self.players = [Player(self), Player(self)]
        # This is the last player atm, because self.next_turn iterates it to the first player when the game starts
        self.current_player_number = len(self.players) - 1
        self.current_player = self.players[self.current_player_number]
        self.current_player.start_turn()

        # the turn which the finish is triggered on (0 if not finished)
        self.finish = 0
        self.objectives_to_win = c.objs_to_win[len(self.players)]

        # -- GAME OBJECTS --

        self.player_label = None
        self.help_text = None
        self.player_info = []

        self.quit_button = None
        # The buttons on the left hand side of the screen (to choose items)
        self.button_system = None

        self.emporer_card = 1

        self.pile_tiles = None
        self.pile_objectives = {}
        self.pile_improvements = {}
        self.pile_rivers = c.max_rivers  # Remember that there are a finite number of rivers
        # The top cards if the user is given a choice (ie to be put at the bottom of the pile)
        self.top_cards = []
        self.to_place = None  # A card for the user to place

        self.improvement_link = {}
        self.objective_link = {}
        self.action_link = []

        self.menu = None
        self.dice = None

        self.panda = None
        self.board = None
        self.gardener = None

        self.create_game_objects()
        self.deal_objectives()

    # -- PYGAME HANDLING --

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

    def update_help(self, text):
        self.help_text.new_text(text)

    # -- OBJECT CREATION --

    def create_game_objects(self):
        self.create_labels()

        self.create_board()
        self.create_characters()
        self.create_weather()
        self.create_piles()
        self.create_player_info()
        self.create_button_system()
        self.create_buttons()

    def create_labels(self):
        self.player_label = TextObject(
            'Player: 1',
            c.player_label_colour,
            10,
            (c.top_bar_height - c.font_size) / 2,
            c.font_size,
        )  # Create text at top of screen saying 'player 1'
        self.player_label.add(self.objects)

        self.help_text = TextObject(
            'Press \'start turn\' to play',
            c.help_colour,
            125,
            (c.top_bar_height - c.font_size) / 2,
            c.font_size)
        self.help_text.add(self.objects)

    def create_buttons(self):
        self.quit_button = Button('quit', c.width - 55, 5, 50, 30, self.b_quit)
        self.quit_button.add(self.objects)

        self.button_system.add_button(
            Button('Start turn', 0, 0, 130, 30, self.next_turn))

    def create_button_system(self):
        self.button_system = ButtonSystem(20, 65)
        self.button_system.add(self.objects)

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

        self.pile_improvements = {  # the improvements that are in the bank (3 for each at the start)
            0: 3,  # irrigation
            1: 3,  # panda
            2: 3  # gardener
        }

    def create_player_info(self):
        for index, i in enumerate(self.players):
            self.player_info.append(PlayerInfo(
                i, c.width - c.player_info_width - 20, (index * (c.player_info_height + 20)) + 150, str(index + 1)))
            self.player_info[-1].add(self.objects)

    # -- BUTTON PRESSED --

    def b_quit(self):
        self.is_game_running = False

    def roll_dice(self):
        return self.dice.roll()

    # -- GAME RULES --

    def deal_objectives(self):
        for player in self.players:
            for objective in self.pile_objectives:
                player.add_objective(self.pile_objectives[objective].take())

    def create_turn_buttons(self):
        self.button_system.add_button(
            Button('end turn', 0, 0, 100, 30, self.next_turn))
        self.button_system.add_button(
            Button('place river', 0, 0, 130, 30, self.place_river))
        self.button_system.add_button(
            Button('place improvement', 0, 0, 180, 30, self.place_improvement))

    def next_turn(self):
        # Increase current_player_number by 1, but cycle it through the total number of players
        self.update_help('')

        self.current_player.finish_turn()

        self.current_player_number = (self.current_player_number + 1) % (
            c.number_of_players
        )
        self.current_player = self.players[self.current_player_number]

        self.player_label.new_text('Player: %s' %
                                   str(self.current_player_number + 1))

        self.current_player.start_turn()

        self.turn_list = ['waiting', 'choose actions']

        if self.turns // len(self.players) >= 1:
            self.turn_list += ['weather', 'roll dice']

        # if self.button_system:  # self.button_system does not exist before the first turn
        self.button_system.remove(self.objects)

        self.turns += 1

        if self.finish != 0:
            # the last round has been triggered
            if self.turns - self.finish >= len(self.players):
                # the final round has finished
                self.end_game()
                self.turn_list = []

        self.create_button_system()
        self.create_turn_buttons()
        self.button_system.disable()

    def clear_menu(self):
        '''clear the menu, and complete the last of "turn_list"'''
        del self.turn_list[-1]
        self.menu.remove(self.objects)
        self.menu = None  # garbage collector should clean this up and delete the object

    def create_action_menu(self):
        '''options = [MenuItem(pygame.image.load(c.image_tiles[0]).convert_alpha()),
                   MenuItem(pygame.image.load(
                       c.image_river).convert_alpha()),
                   MenuItem(pygame.image.load(
                       c.gardener_image).convert_alpha()),
                   MenuItem(pygame.image.load(
                       c.panda_image).convert_alpha()),
                   MenuItem(pygame.image.load(c.objective_image))]'''

        options = []
        toggle_text = []
        self.action_link = []

        if not self.pile_tiles.empty():
            options.append(MenuItem(pygame.image.load(
                c.image_tiles[0]).convert_alpha()))  # place plots
            toggle_text.append('add plot')
            self.action_link.append(0)

        if self.pile_rivers > 0:
            options.append(MenuItem(pygame.image.load(
                c.image_river).convert_alpha()))  # add river
            toggle_text.append('add river')
            self.action_link.append(1)

        options += [MenuItem(pygame.image.load(
            c.gardener_image).convert_alpha()),
            MenuItem(pygame.image.load(
                c.panda_image).convert_alpha())]  # move gardener / move panda
        toggle_text += ['gardener', 'panda']
        self.action_link += [2, 3]

        if not self.current_player.hand.full():
            options.append(MenuItem(pygame.image.load(c.objective_image)))
            toggle_text += ['objective']
            self.action_link.append(4)

        if self.weather != 2:
            self.menu = ChooseMenu(options, 'Choose %i actions' % (
                3 if self.weather == 0 else 2), self, 3 if self.weather == 0 else 2, toggle_text)
        else:
            self.menu = ChooseMenu(
                options, 'Choose 1 action', self, 1, toggle_text)
        self.menu.add(self.objects)

    def create_action_button(self, name):
        button_name = self.button_system.add_button(
            Button(name.capitalize(), 0, 0, len(name) * 13, 30, self.do_action))
        self.button_system.buttons[button_name].add_arguments(
            (button_name, name))

    def do_action(self, args):
        self.update_help('')
        button_name = args[0]
        turn_list_name = args[1]
        self.button_system.disable()
        self.button_system.remove_button(button_name)
        self.turn_list.append(turn_list_name)

    def move_character(self, character, tile):
        if character.move(tile):  # If it was a valid move
            if isinstance(character, Panda):
                bamboo = tile.eat()
                if bamboo is not False:
                    self.current_player.add_bamboo(bamboo)
            else:  # character is gardener
                tile.grow(self.board)

            # Reset game state (character has moved)
            del self.turn_list[-1]
            self.button_system.enable()

    def place_river(self):
        if self.current_player.remove_river():
            self.button_system.disable()
            self.turn_list.append('place river')
        else:
            self.update_help(c.river_warning)

    def place_improvement(self):
        option_images = []
        self.improvement_link = {}

        for i in self.current_player.improvement_reserve:
            if self.current_player.improvement_reserve[i] > 0:
                option_images.append(
                    MenuItem(pygame.image.load(c.improvement_images[i])))
                # key = the index of the improvement in the menu, value = the index of the improvement overall
                self.improvement_link[len(
                    option_images) - 1] = i

        if len(option_images) > 0:
            self.menu = ChooseMenu(
                option_images, 'Choose an improvement', self)
            self.menu.add(self.objects)

            self.turn_list.append('place improvement choice menu')
            self.button_system.disable()
        else:
            self.update_help(c.improvement_warning)

    def trigger_finish(self):
        '''player has copmleted enough objectives - can finish now'''
        if self.emporer_card == 1:
            self.finish = self.turns
            self.current_player.emporer_card()
            self.emporer_card -= 1
            self.update_help(c.trigger_finish)

    def end_game(self):
        ''''''
        winner = None
        winner_points = 0
        for i in self.players:
            if i.points > winner_points:
                winner = i
                winner_points = i.points

        self.update_help('Congratulations! Player %s won with %i points' %
                         (self.players.index(winner) + 1, winner_points))

    # -- MAIN LOOP --

    def run(self):
        # For testing purposes (a sample map):
        '''
        self.board.place(Plot(1, 1, 'green', self.board, 'panda'))
        self.board.place(Plot(0, 1, 'green', self.board))
        self.board.place(Plot(-1, 1, 'green', self.board))
        self.board.place(Plot(0, -1, 'yellow', self.board))
        self.board.place(Plot(-1, 0, 'yellow', self.board))
        self.board.place(Plot(1, 0, 'pink', self.board, 'irrigation'))
        self.board.place(Plot(1, -1, 'pink', self.board))
        '''

        # self.players[0].hand.add_objective(Objective(self.players[0].hand))
        # self.players[0].hand.add_objective(Objective(self.players[0].hand))

        # self.board.river_system.add_river(Cubic(0, 1, 0), Cubic(1, 1, 0))
        # self.next_turn()

        while self.is_game_running:
            # Reset display by rendering the background image
            self.surface.blit(self.background_image, (0, 0))

            self.handle_events()

            # print(self.turn_list)
            if len(self.turn_list) > 0:
                if self.turn_list[-1] == 'weather':

                    if self.weather == 0:  # sun - extra action
                        self.update_help(
                            'Rolled sun - You can choose 3 actions this turn')
                        del self.turn_list[-1]
                    elif self.weather == 1:  # rain
                        self.update_help(
                            'Rolled rain - Choose a tile to add bamboo to')
                        selected_tile = self.board.select_tile()
                        if selected_tile:
                            selected_tile.add_bamboo(1)
                            del self.turn_list[-1]
                    elif self.weather == 2:  # wind - similar action
                        self.update_help(
                            'Rolled wind - You can choose 2 of the same action this turn')
                        del self.turn_list[-1]
                    elif self.weather == 3:  # storm
                        self.update_help(
                            'Rolled storm - Choose a tile to move the panda to')
                        selected_tile = self.board.select_tile()
                        if selected_tile:
                            # If it was a valid move
                            self.panda.transport(selected_tile)
                            bamboo = selected_tile.eat()
                            if bamboo is not False:
                                self.current_player.add_bamboo(bamboo)
                            del self.turn_list[-1]
                    elif self.weather == 4:  # clouds
                        self.update_help(
                            'Rolled clouds - Choose an improvement')
                        option_images = []
                        self.improvement_link = {}

                        for i in self.pile_improvements:
                            if self.pile_improvements[i] > 0:
                                option_images.append(
                                    MenuItem(pygame.image.load(c.improvement_images[i])))
                                # key = the index of the improvement in the menu, value = the index of the improvement overall
                                self.improvement_link[len(
                                    option_images) - 1] = i

                        self.menu = ChooseMenu(
                            option_images, 'Choose 1 improvement', self)
                        self.menu.add(self.objects)

                        del self.turn_list[-1]
                        self.turn_list.append('improvement choice menu')
                    elif self.weather == 5:  # choice
                        self.update_help(
                            'Rolled choice - Choose a weather type')
                        self.menu = ChooseMenu([
                            MenuItem(pygame.image.load(
                                c.weather_images[0]).convert_alpha()),
                            MenuItem(pygame.image.load(
                                c.weather_images[1]).convert_alpha()),
                            MenuItem(pygame.image.load(
                                c.weather_images[2]).convert_alpha()),
                            MenuItem(pygame.image.load(
                                c.weather_images[3]).convert_alpha()),
                            MenuItem(pygame.image.load(c.weather_images[4]).convert_alpha())],
                            'Choose 1 weather system', self, 1, ['Sun', 'Rain', 'Wind', 'Storm', 'Clouds'])
                        self.menu.add(self.objects)
                        self.turn_list.append('weather choice menu')

                elif self.turn_list[-1] == 'roll dice':
                    self.weather = 5
                    del self.turn_list[-1]

                elif self.turn_list[-1] == 'weather choice menu':
                    update = self.menu.update()
                    if update:
                        self.weather = update[0]
                        self.clear_menu()
                        self.dice.update(update[0])

                elif self.turn_list[-1] == 'improvement choice menu':
                    update = self.menu.update()
                    if update:
                        improvement = self.improvement_link[update[0]]
                        self.current_player.add_improvement(improvement)
                        self.pile_improvements[improvement] -= 1

                        self.clear_menu()

                elif self.turn_list[-1] == 'choose actions':

                    del self.turn_list[-1]

                    if self.weather != 2:
                        self.turn_list.append('action choice menu')
                    else:
                        self.turn_list += ['action choice menu',
                                           'action choice menu']

                elif self.turn_list[-1] == 'action choice menu':

                    #self.update_help('Choose your actions')

                    if self.menu:
                        update = self.menu.update()
                        if update:
                            self.clear_menu()
                            self.button_system.enable()

                            actions = {0: 'add plot', 1: 'add river', 2: 'move gardener',
                                       3: 'move panda', 4: 'add objective'}
                            for i in update:
                                self.create_action_button(
                                    actions[self.action_link[i]])
                    else:  # second iteration of this, when wind was the weather
                        self.create_action_menu()

                elif self.turn_list[-1] == 'move panda' or self.turn_list[-1] == 'move gardener':
                    self.update_help('Move the %s in a straight line to a new tile' % (
                        'panda' if self.turn_list[-1] == 'move panda' else 'gardener'))
                    selected_tile = self.board.select_tile()
                    if selected_tile:
                        self.move_character(
                            self.panda if self.turn_list[-1] == 'move panda' else self.gardener, selected_tile)

                elif self.turn_list[-1] == 'add river':
                    if self.pile_rivers > 0:
                        self.current_player.river_reserve += 1
                        self.pile_rivers -= 1
                    else:
                        self.update_help(c.river_reserve_warning)

                    del self.turn_list[-1]
                    self.button_system.enable()

                elif self.turn_list[-1] == 'add plot':
                    del self.turn_list[-1]
                    self.turn_list.append('choose plot menu')

                    for i in range(3 if self.pile_tiles.len() >= 3 else self.pile_tiles.len()):
                        self.top_cards.append(self.pile_tiles.take())

                    # Create menu items:
                    menu_items = []

                    # convert self.top_cards into menu items
                    for i in self.top_cards:
                        # Create a temporary board to hold the tile to choose, then draw it into a 'menu item'
                        board = Board(200, (200, 200))
                        plot = Plot(0, 0, i.colour, board, i.improvement)

                        #  remove all bamboo, incase it has a 'irrigation' improvement and has grown bamboo
                        plot.remove_bamboo(5)
                        board.place(plot)

                        surface = pygame.Surface((400, 400))
                        board.draw(surface)
                        surface.set_colorkey((0, 0, 0))
                        menu_items.append(MenuItem(surface))

                    self.menu = ChooseMenu(
                        menu_items, 'Choose 1 plot to place:', self)
                    self.menu.add(self.objects)

                elif self.turn_list[-1] == 'add objective':
                    if not self.current_player.hand.full():
                        option_images = []
                        self.objective_link = {}

                        for i in self.pile_objectives:
                            if self.pile_objectives[i].len() > 0:
                                option_images.append(
                                    MenuItem(pygame.image.load(c.objectives_images[i])))
                                self.objective_link[len(option_images) - 1] = i

                        self.menu = ChooseMenu(
                            option_images, 'Choose 1 objective', self)
                        self.menu.add(self.objects)

                        del self.turn_list[-1]
                        self.turn_list.append('objective choice menu')
                    else:
                        self.update_help("sorry your hand is full :(")
                        del self.turn_list[-1]

                elif self.turn_list[-1] == 'choose plot menu':
                    update = self.menu.update()
                    if update:
                        self.clear_menu()
                        self.to_place = self.top_cards[update[0]]

                        del self.top_cards[update[0]]
                        for i in self.top_cards:  # add the other two cards back to the pile
                            self.pile_tiles.append(i)

                        self.top_cards = []
                        self.turn_list.append('place plot')

                elif self.turn_list[-1] == 'place plot':
                    self.update_help('Choose a location to place a tile')
                    if self.board.place_tile(self.to_place):
                        # Tile placed
                        self.to_place = None
                        del self.turn_list[-1]
                        self.button_system.enable()

                elif self.turn_list[-1] == 'objective choice menu':
                    update = self.menu.update()
                    if update:
                        self.clear_menu()
                        # add objective using self.objective_link to player hand:
                        objective = self.pile_objectives[self.objective_link[update[0]]].take(
                        )
                        # objective.assign_hand(self.current_player.hand)
                        self.current_player.add_objective(objective)
                        self.button_system.enable()

                elif self.turn_list[-1] == 'place river':
                    if self.board.river_system.place_river():
                        del self.turn_list[-1]
                        self.button_system.enable()

                elif self.turn_list[-1] == 'place improvement choice menu':

                    update = self.menu.update()
                    if update:
                        self.to_place = self.improvement_link[update[0]]
                        self.current_player.remove_improvement(self.to_place)

                        self.clear_menu()
                        self.turn_list.append('place improvement')

                elif self.turn_list[-1] == 'place improvement':

                    update = self.board.select_tile()
                    if update:
                        if not update.has_improvement():
                            if update.bamboo_amount == 0:
                                update.add_improvement(
                                    c.improvements[self.to_place])
                                del self.turn_list[-1]
                                self.button_system.enable()
                            else:
                                self.update_help(
                                    'please choose a different tile - this tile has bamboo')
                        else:
                            self.update_help(
                                'please choose a new tile - this one allready has an improvement')

                elif self.turn_list[-1] == 'waiting':
                    # waiting for the user to do something
                    if self.help_text.text not in c.waiting_warnings:
                        self.update_help('')

            else:
                # Game has ended
                pass

            self.draw()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()


#Main_Game = Game(c.width, c.height)
# Main_Game.run()
