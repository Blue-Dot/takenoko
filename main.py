import pygame
import config as c
from takenoko import Game

width = 1000
height = 600


class Image:
    def __init__(self, image_ref):
        self.image = pygame.image.load(image_ref)
        self.size = self.image.get_size()
        self.coords = pygame.Rect(
            ((width - self.size[0])/2, (height - self.size[1])/2), self.size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.coords.topleft)


class Manager:
    def __init__(self, images):
        self.images = images
        self.image = images[0]
        self.fading = None
        self.alpha = 0
        self.veil = pygame.Surface((width, height))
        self.veil.fill((255, 255, 255))

        self.speed = 32

    def next(self):
        if self.images.index(self.image) < len(self.images) - 1:
            self.fading = 'OUT'
            return True
        return False

    def draw(self, surface):

        if not self.fading:
            # Not transitioning
            pass
        elif self.fading == 'OUT':
            self.alpha += self.speed
            if self.alpha >= 255:
                self.fading = 'IN'
                self.image = self.images[self.images.index(self.image) + 1]
        elif self.fading == 'IN':
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.fading = None
                self.alpha = 0

        self.image.draw(surface)
        self.veil.set_alpha(self.alpha)
        surface.blit(self.veil, (0, 0))


pygame.init()
main_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Takenoko Story')

loop = True
leave = False

pictures = []
for i in range(1, 7):
    pictures.append(Image('images/comics/' + str(i) + '.png'))

manager = Manager(pictures)

clock = pygame.time.Clock()

while loop and not leave:
    main_surface.fill((251, 241, 223))

    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            leave = True
        if e.type == pygame.KEYDOWN:
            if not manager.next():
                loop = False

    manager.draw(main_surface)

    pygame.display.flip()
    clock.tick(c.frame_rate)

pygame.quit()

if not leave:
    Main_Game = Game(c.width, c.height)
    Main_Game.run()

