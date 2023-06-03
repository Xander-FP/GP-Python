# A class called NonTerminals that contains all the non-terminals in the grammar
from Node import *

class NonTerminal:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def getNumRules(self):
        pass
    
    def applyRule(self, rule):
        pass
    
class Expr(NonTerminal):
    def __init__(self):
        super().__init__('<expr>')
        self.numRules = 2

    def __str__(self):
        return '<expr>'

    def getNumRules(self):
        return self.numRules
    
    def applyRule(self, rule):
        if rule == 0:
            return [Op(), Expr(), Expr()]
        elif rule == 1:
            return [Var()]

class Op(NonTerminal):
    def __init__(self):
        super().__init__('<op>')
        self.numRules = 4

    def __str__(self):
        return '<op>'

    def getNumRules(self):
        return [self.numRules]

    def applyRule(self, rule, parent = None):
        if rule == 0:
            return [Add(parent)]
        elif rule == 1:
            return [Subtract(parent)]
        elif rule == 2:
            return [Multiply(parent)]
        elif rule == 3:
            return [Divide(parent)]

class Var(NonTerminal):
    def __init__(self):
        super().__init__('<var>')
        self.numRules = 10

    def __str__(self):
        return '<var>'

    def getNumRules(self):
        return self.numRules

    def applyRule(self, rule):
        if rule == 0:
            return [Terminal('Distance')]
        elif rule == 1:
            return [Terminal('Haversine')]
        elif rule == 2:
            return [Terminal('Wind')]
        elif rule == 3:
            return [Terminal('Snow')]
        elif rule == 4:
            return [Terminal('Precip')]
        elif rule == 5:
            return [Terminal('GroundTemp')]
        elif rule == 6:
            return [Terminal('Dust')]
        elif rule == 7:
            return [Terminal('Humid')]
        elif rule == 8:
            return [Terminal('Solar')]
        elif rule == 9:
            return [Terminal('Temp')]