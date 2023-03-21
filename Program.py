from __future__ import annotations
from Node import Node

class Program:
    def __init__(self, max_depth = None):
        self.__head = Node(None, False)
        if max_depth != None:
            self.__head.generate(max_depth)
        self.__hits = 0
        self.__fitness = 0

    def getHead(self):
        return self.__head
    
    def resetHits(self):
        self.__hits = 0
    
    def getHits(self):
        return self.__hits
    
    def addHit(self):
        self.__hits += 1

    def getFitness(self):
        return self.__fitness
    
    def addFitness(self,__fitness):
        self.__fitness += __fitness

    def assignFitness(self,tuple):
        self.__fitness = tuple[1]
        self.__hits = tuple[2]

    def clone(self) -> Program:
        new_program = Program()
        queue = [self.__head]
        queue.append(new_program.getHead())
        while (len(queue) > 0):
            el = queue.pop(0)
            curr_node = queue.pop(0)
            curr_node.setVal(el.getVal())
            curr_node.setNumChildren(el.getNumChildren())
            for child in el.getChildren():
                new_child = Node(curr_node,child.isTerminal())
                curr_node.appendChild(new_child)
                queue.append(child)
                queue.append(new_child)
        new_program.resetHits()
        return new_program
    
    def updateLevel(self):
        self.__head.updateLevel()
    
    def calcNumChildren(self):
        self.__head.setNumChildren(self.__head.calcNumChildren())
        return self.__head.getNumChildren()
    
    def prune(self, max_depth):
        self.__head.prune(max_depth, 0)

    def __str__(self):
        self.updateLevel()
        queue = [self.__head]
        curr_level = 1
        result = str(curr_level) + ':'
        while (len(queue) > 0):
            el = queue.pop(0)
            for node in el.getChildren():
                queue.append(node)
            if (curr_level == el.getLevel()):
                result += el.getVal() + ' '
            else:
                curr_level = el.getLevel()
                result += '\n' + str(curr_level) + ':' + el.getVal() + ' '


        return result
    
    def __ge__(self, other):
        if ( self.getFitness() > other.getFitness()):
                return False
        else:
            if (self.getFitness() == other.getFitness):
                if (self.getHits() < other.getHits()):
                    return False
        return True
    
    def __eq__(self,other):
        if (other == None):
            return False
        return round(self.getFitness(),1) == round(other.getFitness(),1)