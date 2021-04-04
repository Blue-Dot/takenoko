import random
import config as c
from objectives import Panda, Gardener
from plots import FloatingPlot

class Pile():
    '''effectively a queue: FIFO'''
    def __init__(self, default=None):
        '''default is list'''
        self.pile = []
        if default is not None:
            flavour = default[0]["id"][0:2]
            if flavour == "TI": #This is a tile pile (for all the plots):
                for i in default:
                    self.pile.append(FloatingPlot(i["colour"], i["improvements"]))
            elif flavour == "PA": #Objective pile (for panda objectives)
                for i in default:
                    self.pile.append(Panda(i["points"], i["bamboo"], None))
            elif flavour == "GA": #Objective pile (for gardener objectives)
                for i in default:
                    self.pile.append(Gardener(i["points"], i["bamboo"], None))
            elif flavour == "PL": #Objective pile (for plot objectives)
                pass
            #self.pile = default
    
    def empty(self):
        '''is the pile empty: returns boolean'''
        if len(self.pile) > 0:
            return False
        return True
    
    def take(self):
        '''Take from the top of the pile (ie first in)'''
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

