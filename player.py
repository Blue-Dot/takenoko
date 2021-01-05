class Player:
    def __init__(self):
        self.river_reserve = 0
        self.bamboo_reserve = []
    
    def remove_river(self):
        if self.river_reserve > 0:
            self.river_reserve -= 1
        else:
            return False

    def add_bamboo(self, colour):
        self.bamboo_reserve.append(colour)
