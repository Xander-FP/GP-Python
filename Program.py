from __future__ import annotations
from Node import Node

class Program:
    def __init__(self, max_depth = None):
        self.__current_similarity = 0
        self.__head = Node.generateNode(None, False)
        if max_depth != None:
            self.__head.generate(max_depth)
        self.__hits = 0
        self.__fitness = 0

    def getHead(self):
        return self.__head
    
    def setHead(self, head):
        self.__head = head
    
    def resetHits(self):
        self.__hits = 0
    
    def getHits(self):
        return self.__hits
    
    def addHit(self):
        self.__hits += 1

    def getFitness(self):
        return self.__fitness
    
    def addFitness(self,fitness):
        self.__fitness += fitness

    def assignFitness(self,tuple):
        self.__fitness = tuple[1]
        self.__hits = tuple[2]

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
    
    def getSimilarity(self):
        return self.__current_similarity
    
    def setSimilarity(self, sim):
        self.__current_similarity = sim

    # Function compares current program to other program and keeps on counting similarity until there are no more matches
    def calculateSimilarity(self, other):
        similarity = 0
        queue = [self.__head]
        queue.append(other.getHead())
        while (len(queue) > 0):
            curr_node = queue.pop(0)
            other_node = queue.pop(0)
            if (curr_node == other_node):
                similarity += 1
                curr_children = curr_node.getChildren()
                other_children = other_node.getChildren()
                queue.append(curr_children[0])
                queue.append(other_children[0])
                if (len(curr_children) > 1):
                    queue.append(curr_children[1])
                else:
                    queue.append(None)
                if (len(other_children) > 1):
                    queue.append(other_children[1])
                else:
                    queue.append(None)
        self.__current_similarity = similarity
        return similarity

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
        if ( self.getFitness() >= other.getFitness()):
                return False
        return True
    
    def __eq__(self,other):
        if (other == None):
            return False
        return round(self.getFitness(),1) == round(other.getFitness(),1)