import pygame
import config as c

class TextObject(pygame.sprite.Sprite):
    def __init__(self, text, colour, x, y, size):
        super().__init__()
        self.coords = (x, y)
        self.text = text
        self.colour = colour
        self.font = pygame.font.SysFont(c.font_name, size)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.colour)
        surface.blit(text_surface, self.coords)
    
    def new_text(self, text):
        self.text = text