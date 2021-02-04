import pygame
import random

#My imports
import config as c
from player import Player
from text_object import TextObject
from button import Button
from plots import Pond, Plot
from board import MainBoard
from characters import Panda, Gardener

class Game:
    def __init__(self, width, height):

        # -- GENERAL GAME SETUP --

        self.width, self.height = width, height

        pygame.init()
        pygame.font.init()

        self.surface = pygame.display.set_mode((width, height))

        self.background_image = self.tile_background(pygame.image.load(c.background_image).convert()) #Generate background image by tiling pattern
        self.frame_rate = c.frame_rate
        self.objects = pygame.sprite.Group() #All game objects
        self.is_game_running = True 
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(c.caption)

        # -- SPEFICIC TAKENOKO SETUP -- 

        self.game_state = "" #CURRENT GAME STATE(!!)

        self.players = [Player(), Player()]
        self.current_player_number = 0
        self.current_player = self.players[self.current_player_number]

        # -- GAME OBJECTS --

        #Buttons
        self.player_label = None
        self.quit_button = None
        self.eat_button = None
        self.grow_button = None
        self.next_turn_button = None

        self.board = None

        self.create_game_objects()
        
    def tile_background(self, tile):
        #Tile background image and store in a surface
        background = pygame.Surface((self.width, self.height))
        for h in range(self.width + tile.get_width() - 1 // tile.get_width()): #This is ceiling division, just without importing 'math'
            for w in range(self.height + tile.get_height() - 1 // tile.get_height()):
                background.blit(tile, (w * tile.get_width(), h * tile.get_height())) #Blit the tile onto the correct spot
        pygame.draw.rect(background, c.top_bar_colour, pygame.Rect(0, 0, self.width, c.top_bar_height))
        pygame.draw.rect(background, c.top_bar_outline_colour, pygame.Rect(0, c.top_bar_height, self.width, c.top_bar_outline_thickness))
        return background

    def draw(self):
        for spr in self.objects.sprites():
            spr.draw(self.surface)
        #self.objects.draw(self.surface)

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

    def create_labels(self):
        self.player_label = TextObject('Player: 1', c.player_label_colour, 10, (c.top_bar_height - c.font_size)/2, c.font_size) #Create text at top of screen saying 'player 1'
        self.player_label.add(self.objects)

    def create_buttons(self):
        self.quit_button = Button('quit', c.width - 55, 5, 50, 30, self.b_quit)
        self.quit_button.add(self.objects)

        self.eat_button = Button('eat', 20, 65, 50, 30, self.b_eat)
        self.eat_button.add(self.objects)

        self.grow_button = Button('grow', 20, 65 + 50, 50, 30, self.b_grow)
        self.grow_button.add(self.objects)

        self.next_turn_button = Button('next turn', 20, 165, 90, 30, self.next_turn)
        self.next_turn_button.add(self.objects)

        self.panda_move_button = Button('move panda', 20, 165 + 50, 120, 30, self.b_panda_move)
        self.panda_move_button.add(self.objects)

        self.gardener_move_button = Button('move gardener', 20, 265, 150, 30, self.b_gardener_move)
        self.gardener_move_button.add(self.objects)

    def create_board(self):
        self.board = MainBoard(c.hexagon_size, c.board_center)
        self.board.place(Pond(0, 0))
        self.board.add(self.objects)

    def create_characters(self):
        self.panda = Panda(c.hexagon_size, c.board_center)
        self.gardener = Gardener(c.hexagon_size, c.board_center)
        self.panda.add(self.objects)
        self.gardener.add(self.objects)

    # -- BUTTON PRESSED --

    def b_quit(self):
        self.is_game_running = False

    def b_eat(self):
        self.game_state = 'eat'

    def b_grow(self):
        self.game_state = 'grow'
    
    def b_panda_move(self):
        self.game_state = 'move panda'

    def b_gardener_move(self):
        self.game_state = 'move gardener'

    # -- GAME RULES --

    def next_turn(self):
        self.current_player_number = (self.current_player_number + 1) % (c.number_of_players) #Increase current_player_number by 1, but cycle it through the total number of players
        self.current_player = self.players[self.current_player_number]

        self.player_label.new_text('Player: %s' % str(self.current_player_number + 1))

    def run(self):
        #For testing purposes (a sample map):
        self.board.place(Plot(1, 1, 'green'))
        self.board.place(Plot(0, 1, 'green'))
        self.board.place(Plot(-1, 1, 'green'))
        self.board.place(Plot(0, -1, 'yellow'))
        self.board.place(Plot(-1, 0, 'yellow'))
        self.board.place(Plot(1, 0, 'pink'))
        self.board.place(Plot(1, -1, 'pink'))

        
        while self.is_game_running:
            self.surface.blit(self.background_image, (0, 0)) #Reset display by rendering the background image

            self.handle_events()
            
            print(self.game_state)

            if self.game_state == 'grow':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    selected_tile.grow()
            elif self.game_state == 'eat':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    selected_tile.remove_bamboo(1)
            elif self.game_state == 'move panda':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    if self.panda.move(selected_tile): #If it was a valid move
                        selected_tile.eat()
                        self.game_state = '' #Reset game state (panda has moved)
            elif self.game_state == 'move gardener':
                selected_tile = self.board.select_tile()
                if selected_tile:
                    if self.gardener.move(selected_tile): #If it was a valid move
                        selected_tile.grow(self.board)
                        self.game_state = '' #Reset game state (gardener has moved)

            self.draw()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        pygame.quit()

Main_Game = Game(c.width, c.height)

Main_Game.run()
