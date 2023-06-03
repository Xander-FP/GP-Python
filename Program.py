from __future__ import annotations
from Node import Node

class Program:
    def __init__(self):
        self.__fitness = 0

    def getHead(self):
        return self.__head
    
    def setHead(self, head):
        self.__head = head
    
    def getFitness(self):
        return self.__fitness
    
    def addFitness(self,fitness):
        self.__fitness += fitness

    def clone(self) -> Program:
        new_program = Program()
        new_program.setHead(self.__head.clone(None))
        queue = [self.__head]
        queue.append(new_program.getHead())
        while (len(queue) > 0):
            parent = queue.pop(0)
            curr_node = queue.pop(0)
            curr_node.setNumChildren(parent.getNumChildren())
            for child in parent.getChildren():
                new_child = child.clone(curr_node)
                curr_node.appendChild(new_child)
                queue.append(child)
                queue.append(new_child)
        new_program.resetHits()
        return new_program
    
    def updateLevel(self):
        self.__head.setLevel(1)
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
    
    def __ge__(self, other) -> bool:
        if ( self.getFitness() >= other.getFitness()):
                return False
        return True
    
    def __eq__(self,other) -> bool:
        if (other == None):
            return False
        return round(self.getFitness()) == round(other.getFitness())
    
    def __hash__(self) -> int:
        return round(self.getFitness())