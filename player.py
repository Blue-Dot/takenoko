from objectives import Hand, Objective

class Player:
    def __init__(self, game):
        self.game = game
        self.hand = Hand(self.game)

        self.river_reserve = 0
        self.bamboo_reserve = []
    
    def draw(self, surface):
        self.hand.draw(surface)

    def remove_river(self):
        if self.river_reserve > 0:
            self.river_reserve -= 1
        else:
            return False

    def add_bamboo(self, colour):
        self.bamboo_reserve.append(colour)
    
    def complete_objective(self, objective):
        pass
