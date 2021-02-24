import random

class Pile():
    '''effectively a queue: FIFO'''
    def __init__(self, default=None):
        '''default is list'''
        if default is None:
            self.pile = []
        else:
            self.pile = default
    
    def empty(self):
        if len(self.pile) > 0:
            return False
        return True
    
    def take(self):
        if not self.empty():
            card = self.pile[0]
            self.pile = self.pile[1:]
            return card
        else:
            raise Exception("this pile is empty")
    
    def append(self, card):
        self.pile.append(card)

    def shuffle(self):
        random.shuffle(self.pile)
        return self
    
