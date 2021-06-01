import pygame
import config as c


class TextObject(pygame.sprite.Sprite):
    def __init__(self, text, colour, x, y, size):
        super().__init__()
        self.text = text
        self.colour = colour
        self.font = pygame.font.SysFont(c.font_name, size)

        self.image = self.font.render(self.text, True, self.colour)
        self.rect = pygame.rect.Rect(
            (x, y), (self.image.get_height(), self.image.get_width()))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def new_text(self, text):
        if self.text != text:
            self.text = text
            self.image = self.font.render(self.text, True, self.colour)
