import pygame
import config as c
from text_object import TextObject
import colours
from button import Button, Toggle


class ChooseMenu(pygame.sprite.Sprite):
    def __init__(self, choices, text, game, number=1, toggle_text=None):
        super().__init__()
        self.size = (len(choices)*150, c.choose_menu_height)
        self.choices = choices
        self.number = number
        print(self.number)

        self.game = game

        self.toggles = []
        if not toggle_text:
            self.toggle_text = ['pick'] * len(self.choices)
        else:
            self.toggle_text = toggle_text

        self.shadow = pygame.surface.Surface(self.size)
        self.shadow.fill(c.shadow_colour)

        self.rect = pygame.rect.Rect(
            ((c.width - self.size[0]) // 2, (c.height - self.size[1]) // 2), self.size)

        self.create_surface(choices, text)

        self.complete = False
        self.done_button = Button(
            'Done', self.rect.centerx - 27, self.rect.bottom - 45, 55, 30, self.done)
        self.selected_options = []

    def create_surface(self, choices, text):
        '''create the surface and buttons'''
        self.surface = pygame.surface.Surface(self.size)
        self.surface.fill(c.objective_colour)

        self.text = TextObject(text, colours.WHITE, 10, 10, 20)
        self.text.draw(self.surface)

        for index, i in enumerate(choices):
            location = (150 * index + 75, 100)
            i.draw(self.surface, location)

            text = self.toggle_text[index]
            width = len(text) * 12 if len(text) * 12 > 80 else 80
            toggle_location_x = self.rect.left + \
                index * 150 + (150 - width) // 2
            toggle_location_y = self.rect.top + 150
            self.toggles.append(
                Toggle(toggle_location_x, toggle_location_y, width, 30, text))

    def draw(self, surface):
        surface.blit(
            self.shadow, (self.rect.topleft[0] + 5, self.rect.topleft[1] + 5))
        surface.blit(self.surface, self.rect.topleft)

        for i in self.toggles:
            i.draw(surface)

        self.done_button.draw(surface)

    def done(self):
        self.selected_options = []

        for index, i in enumerate(self.toggles):
            if i.get_state():
                self.selected_options.append(index)

        if len(self.selected_options) == self.number:
            self.complete = True
        else:
            self.game.update_help('you selected %i options, when you should have selected %i options' % (
                len(self.selected_options), self.number))

    def update(self):
        if self.complete:
            return self.selected_options


class MenuItem:
    '''the image for each item in the menu'''

    def __init__(self, image):
        self.surface = image

        width = self.surface.get_width()
        height = self.surface.get_height()
        self.size = ((70 * width) // height, 70)
        self.surface = pygame.transform.scale(self.surface, self.size)

    def draw(self, surface, location):
        location = (location[0] - (self.size[0] // 2),
                    location[1] - (self.size[1] // 2))
        surface.blit(self.surface, location)
