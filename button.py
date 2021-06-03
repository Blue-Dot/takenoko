import pygame
from text_object import TextObject
import config as c


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height, on_click, arguments=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.size = (width, height)
        self.text = text

        self.text_colour = c.button_text_colour
        self.colour = c.button_colour
        self.hover_colour = c.button_hover_colour
        self.click_colour = c.button_click_colour

        self.pressed = False
        self.on_click = on_click
        self.arguments = arguments

        self.create_surface(self.colour, self.text_colour)

    def draw(self, surface):
        self.check_mouse()
        surface.blit(self.surface, (self.rect.topleft))

    def create_surface(self, colour, text_colour):
        self.text_object = TextObject(
            self.text, text_colour, 5, ((self.size[1] - 20) / 2), 20)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(colour)
        self.text_object.draw(self.surface)

    def check_mouse(self):  # TESTED - Works!
        # Cursor is over the button
        if self.rect.collidepoint(pygame.mouse.get_pos()) == True:
            if pygame.mouse.get_pressed()[0] == True:  # Buttton 1 is pressed
                self.pressed = True
                self.create_surface(self.click_colour, self.text_colour)
            else:  # Button 1 is not pressed
                if self.pressed:  # Ie just released
                    if self.arguments:
                        self.on_click(self.arguments)
                    else:
                        self.on_click()
                self.pressed = False
                self.create_surface(self.hover_colour, self.text_colour)
        else:
            self.pressed = False
            # Reset to normal
            self.create_surface(self.colour, self.text_colour)

    def move_to(self, x, y):
        '''move the button'''
        self.rect = self.rect.move(x - self.rect.x, y - self.rect.y)

    def add_arguments(self, arguments):
        self.arguments = arguments


class Toggle(Button):
    def __init__(self, x, y, width, height, text='pick'):
        super().__init__(text, x, y, width, height, self.click)
        self.state = False

    def click(self):
        if self.state is True:
            self.state = False
            self.colour = c.button_colour
            self.hover_colour = c.button_hover_colour
        else:
            self.state = True
            self.colour = c.toggle_selected_colour
            self.hover_colour = c.toggle_hover_selected_colour

        self.create_surface(self.colour, self.text_colour)

    def get_state(self):
        return self.state


class ButtonSystem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.coords = pygame.rect.Rect((x, y), (0, 0))
        self.buttons = {}
        self.enabled = True
        self.identifier = 0

    def draw(self, surface):
        if self.enabled:
            buttons = self.buttons.copy() # this is needed because self.buttons can change during 'run' (ie if a button is deleted)
            for i in buttons:
                self.buttons[i].draw(surface)

    def add_button(self, button):
        '''add a button to the button system - returns id'''
        self.identifier += 1
        button.move_to(self.coords.x, self.coords.y + 50 * len(self.buttons))
        self.buttons[self.identifier] = button
        return self.identifier


    def remove_button(self, name):
        del self.buttons[name]

        for index, i in enumerate(self.buttons):
            self.buttons[i].move_to(self.coords.x, self.coords.y + 50 * index)

    def disable(self):
        '''disables the system so that the buttons aren't drawn, and cannot be pressed'''
        self.enabled = False

    def enable(self):
        '''enables the system so that the buttons are drawn and active'''
        self.enabled = True

    def clear(self):
        self.buttons = {}
