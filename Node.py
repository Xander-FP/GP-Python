from __future__ import annotations
from typing import List
import GlobalVariables as global_vars

class Node:
    def __init__(self, parent: Node, is_terminal: bool) -> None:
        self.__num_children = 0
        self.__is_terminal = is_terminal
        self.__children:List[Node] = []
        self.__parent = parent
        if (not parent == None):
            self.__level = parent.getLevel() + 1
        else:
            self.__level = 1

    @staticmethod
    def generateNode(parent:Node, terminal:bool = None)-> Node:
        if terminal == None:
            terminal = Node.__determinIfIsTerminal()
        if not terminal:
            function = global_vars.function_set[global_vars.num.randrange(len(global_vars.function_set))]
            if function == '+':
                return Add(parent)
            if function == '-':
                return Subtract(parent)
            if function == 'x':
                return Multiply(parent)
            if function == '/':
                return Divide(parent)
            
        return Terminal(parent)

    def generate(self, maxdepth):# A recursive function to generate the trees
        if (not self.__is_terminal):
            if (self.__level >= maxdepth - 1):
                node1 = self.generateNode(self, True)
                if (not self.getVal() == 'sqr' and not self.getVal() == 'sqrt'):
                    node2 = self.generateNode(self, True)
            else:
                node1 = self.generateNode(self, self.__determinIfIsTerminal())
                node1.generate(maxdepth)
                if (not self.getVal() == 'sqr' and not self.getVal() == 'sqrt'):
                    node2 = self.generateNode(self, self.__determinIfIsTerminal())
                    node2.generate(maxdepth)
            self.__children.append(node1)
            self.__num_children += node1.__num_children + 1
            if (not self.getVal() == 'sqr' and not self.getVal() == 'sqrt'):
                self.__children.append(node2)
                self.__num_children += node2.__num_children + 1

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
        print('getVal Not implemented for this class')
        return self.__value
    
    def setVal(self, new_val):
        print('setVal Not implemented for this class')
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
        return False
    
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

    def getParent(self):
        return self.__parent
    
    def setParent(self, parent:Node):
        self.__parent = parent

    def performOperation(self, val1, val2):
        print('performOperation not implemented for class')

    @staticmethod
    def __determinIfIsTerminal():
        return global_vars.num.random() > global_vars.terminal_bound
         
    def __str__(self) -> str:
        return self.getVal()
    
    def __eq__(self, other:Node):
        if other == None:
            return False
        return self.getVal() == other.getVal()
    
    def clone(self, parent):
        print('abstract Node class for clone')
    
# ************************************************************** SUB CLASSES **************************************************
class Add(Node):
    def __init__(self, parent):
        super().__init__(parent, False)

    def performOperation(self, val1, val2):
        return val1 + val2
    
    def getVal(self) -> str:
        return '+'
    
    def clone(self, parent):
        return Add(parent)

class Subtract(Node):
    def __init__(self, parent):
        super().__init__(parent, False)

    def performOperation(self, val1, val2):
        return val1 - val2
    
    def getVal(self) -> str:
        return '-'
    
    def clone(self, parent):
        return Subtract(parent)

class Multiply(Node):
    def __init__(self, parent):
        super().__init__(parent, False)

    def performOperation(self, val1, val2):
        return val1 * val2
    
    def getVal(self) -> str:
        return '*'
    
    def clone(self, parent):
        return Multiply(parent)

class Divide(Node):
    def __init__(self, parent):
        super().__init__(parent, False)

    def performOperation(self, val1, val2):
        if (val2 == 0):
            return 1
        return val1 / val2
    
    def getVal(self) -> str:
        return '/'
    
    def clone(self, parent):
        return Divide(parent)

class Terminal(Node):
    def __init__(self, parent):
        self.__value = self.__selectTerminal()
        super().__init__(parent, True)

    def performOperation(self, val1, val2):
        print('class = Terminal')
        return super().performOperation(val1, val2)
    
    def getVal(self) -> str:
        return self.__value
    
    def setVal(self, new_val):
        self.__value = new_val

    def isTerminal(self):
        return True
    
    def __selectTerminal(self):
        return global_vars.terminal_set[global_vars.num.randrange(len(global_vars.terminal_set))]
    
    def clone(self, parent):
        new_node = Terminal(parent)
        new_node.setVal(self.getVal())
        return new_node

# ******************************************** NOT USED IN CURRENT IMPLEMENTATION *******************************************************

class Square(Node):
    def __init__(self, parent):
        super().__init__(parent, False)

    def performOperation(self, val1, val2 = 0):
        return val1 * val1
    
    def getVal(self) -> str:
        return 'sqr'