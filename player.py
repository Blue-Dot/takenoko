from objectives import Hand


class Player:
    def __init__(self, game):
        self.game = game
        self.hand = Hand(self.game)

        self.river_reserve = 0
        self.bamboo_reserve = []
        # 1 = irrigation, 2 = panda, 3 = gardener
        self.improvement_reserve = {0: 0, 1: 0, 2: 0}

        self.turn = False  # is it my turn?

        self.points = 0
        self.completed_objectives = 0

    def draw(self, surface):
        self.hand.draw(surface)

    def add_river(self, num):
        self.river_reserve += num

    def remove_river(self):
        if self.river_reserve > 0:
            self.river_reserve -= 1
            return True
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
                return True
            else:
                return False

        self.bamboo_reserve = reserve
        return True

    def complete_objective(self, objective):
        self.points += objective.points
        self.completed_objectives += 1

        if self.completed_objectives >= self.game.objectives_to_win:
            self.game.trigger_finish()

    def start_turn(self):
        self.turn = True

    def finish_turn(self):
        self.turn = False

    def add_improvement(self, improvement):
        self.improvement_reserve[improvement] += 1

    def remove_improvement(self, improvement):
        self.improvement_reserve[improvement] -= 1

    def add_objective(self, objective):
        self.hand.add_objective(objective)

    def emporer_card(self):
        # First player to finish gets 2 extra points
        self.points += 2