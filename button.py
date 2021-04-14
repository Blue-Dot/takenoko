import pygame
from text_object import TextObject
import config as c


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height, on_click):
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


class Toggle(Button):
    def __init__(self, x, y, width, height):
        super().__init__('pick', x, y, width, height, self.click)
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
