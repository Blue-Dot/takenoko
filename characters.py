import pygame
import config as c
import coordinates

class Character(pygame.sprite.Sprite):
    def __init__(self, hexagon_size, board_center):
        self.board_center = board_center #The center of the board in cartesian coords (ie half height and half width)
        self.hexagon_size = hexagon_size

        super().__init__() #Calles the Sprite class __init__
        self.coords = coordinates.Axial(0, 0)
        self.surface = None

    def draw(self, surface):
        surface.blit(self.surface, self.get_coords())

    def get_coords(self):
        pass

    def move(self, destination):
        if self.check_move(destination):
            self.transport(destination)
            return True #Valid mvove
        return False #Invalid move

    def transport(self, destination): #Move with no checks
        self.coords = destination.axial
        
    def check_move(self, destination):
        #Check if the destination and current position are in a straight line:
        if self.coords.r == destination.axial.r or self.coords.s == destination.axial.s or self.coords.q == destination.axial.q:
            if self.coords != destination.axial: #Check the destination tile is a different tile
                return True
        return False

class Panda(Character):
    def __init__(self, hexagon_size, board_center):
        super().__init__(hexagon_size, board_center)

        self.surface = pygame.image.load(c.panda_image)
        self.surface = pygame.transform.scale(self.surface, (c.panda_width, c.panda_height))

    def get_coords(self):
        return (self.coords.cartesian(self.hexagon_size, self.board_center)[0], self.coords.cartesian(self.hexagon_size, self.board_center)[1])

class Gardener(Character):
    def __init__(self, hexagon_size, board_center):
        super().__init__(hexagon_size, board_center)

        self.surface = pygame.image.load(c.gardener_image)
        self.surface = pygame.transform.scale(self.surface, (c.gardener_width, c.gardener_height))
    
    def get_coords(self): #Displaces the gardener a little bit so it doesn't overlap with the panda
        return (self.coords.cartesian(self.hexagon_size, self.board_center)[0], self.coords.cartesian(self.hexagon_size, self.board_center)[1]  - self.hexagon_size / 2) 
