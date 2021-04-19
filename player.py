from objectives import Hand


class Player:
    def __init__(self, game):
        self.game = game
        self.hand = Hand(self.game)

        self.river_reserve = 0
        self.bamboo_reserve = []
        self.improvement_reserve = []

        self.turn = False  # is it my turn?

        self.points = 0
        # - weather
        # - action:
        #   - plot
        #   - river
        #   - gardener
        #   - panda
        #   - objective
        # - place:
        #   - river
        #   - improvement

    def draw(self, surface):
        self.hand.draw(surface)

    def remove_river(self):
        if self.river_reserve > 0:
            self.river_reserve -= 1
        else:
            return False

    def add_bamboo(self, colour):
        self.bamboo_reserve.append(colour)

    def trade_bamboo(self, bamboo):
        """check if bamboo (a list) is in reserve. removes bamboo if it is valid. returns boolean"""
        reserve = self.bamboo_reserve.copy()
        for i in bamboo:
            if i in reserve:
                reserve.remove(i)
            else:
                return False

        self.bamboo_reserve = reserve
        return True

    def complete_objective(self, objective):
        self.points += objective.points

    def start_turn(self):
        self.turn = True

    def finish_turn(self):
        self.turn = False
