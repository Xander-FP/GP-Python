from __future__ import annotations
from typing import List
import GlobalVariables as global_vars

class Node:
    def __init__(self, parent, is_terminal) -> None:
        self.__num_children = 0
        self.__is_terminal = is_terminal
        self.__children:List[Node] = []
        if (is_terminal):
            self.__value = self.__selectTerminal()
        else:
            self.__value = self.__selectFunction()
        self.__parent = parent
        if (not parent == None):
            self.__level = parent.getLevel() + 1
        else:
            self.__level = 1

    def generate(self, maxdepth):# A recursive function to generate the trees
        if (not self.__is_terminal):
            if (self.__level >= maxdepth - 1):
                node1 = Node(self, True)
                if (not self.__value == 'sqr' and not self.__value == 'sqrt'):
                    node2 = Node(self, True)
            else:
                node1 = Node(self, self.__determinIfIsTerminal())
                node1.generate(maxdepth)
                if (not self.__value == 'sqr' and not self.__value == 'sqrt'):
                    node2 = Node(self, self.__determinIfIsTerminal())
                    node2.generate(maxdepth)
            self.__children.append(node1)
            self.__num_children += node1.__num_children + 1
            if (not self.__value == 'sqr' and not self.__value == 'sqrt'):
                self.__children.append(node2)
                self.__num_children += node2.__num_children + 1

    def mutate(self, max_depth):
        self.__is_terminal = self.__determinIfIsTerminal()
        if (self.__is_terminal):
            self.__value = self.__selectTerminal()
        else:
            self.__value = self.__selectFunction()
        self.generate(max_depth)

    def updateLevel(self):
        for child in self.__children:
            child.setLevel(self.getLevel() + 1)
            child.updateLevel()

    def prune(self, max_level, curr_level):
        if curr_level >= max_level:
            if not self.isTerminal():
                self.__value = self.__selectTerminal()
            self.setChildren([])
        else:
            for child in self.__children:
                child.prune(max_level, curr_level + 1)

    
    def calcNumChildren(self):
        if (self.isTerminal()):
            return 0
        if len(self.__children) == 2:
            return self.__children[1].calcNumChildren() + self.__children[0].calcNumChildren() + 2
        return self.__children[0].calcNumChildren() + 1
        

    def getVal(self) -> str:
        return self.__value
    
    def setVal(self, new_val):
        self.__value = new_val
    
    def getChildren(self) -> List[Node]:
        return self.__children
    
    def setChildren(self, children):
        if len(children) == 0:
            self.__is_terminal = True
        else:
            self.__is_terminal = False
        self.__children = children

    def appendChild(self, child):
        self.__children.append(child)
    
    def isTerminal(self):
        return self.__is_terminal
    
    def setTerminal(self, val):
        self.__is_terminal = val
    
    def getLevel(self):
        return self.__level
    
    def setLevel(self, level):
        self.__level = level
    
    def getNumChildren(self):
        return self.__num_children
    
    def setNumChildren(self, num):
        self.__num_children = num

    def __determinIfIsTerminal(self):
        return global_vars.num.random() > global_vars.terminal_bound
         
    def __selectTerminal(self):
        return global_vars.terminal_set[global_vars.num.randrange(len(global_vars.terminal_set))]


    def __selectFunction(self):
        return global_vars.function_set[global_vars.num.randrange(len(global_vars.function_set))]
    
    def __str__(self) -> str:
        return self.__value
    
    def __eq__(self, other:Node):
        return self.getVal() == other.getVal()
    