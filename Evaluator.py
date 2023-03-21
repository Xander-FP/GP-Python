import math
from Node import Node
class Evaluator:

    def evaluate(self, program, data_set):
        self.__data_set = data_set
        return self.__evaluate(program.getHead())

    # Recursive private function to evaluate the tree
    def __evaluate(self,current:Node):
        if(current.isTerminal()):
            return self.__getValue(current.getVal())
        children = current.getChildren()
        if (len(children) == 1):
            return self.__performOperation(current.getVal(), self.__evaluate(children[0]))
        return self.__performOperation(current.getVal(), self.__evaluate(children[0]), self.__evaluate(children[1]))
        
    def __getValue(self, item):
        return self.__data_set[item]

    def __performOperation(self, op, val1, val2 = 0):
        match op:
            case '+':
                return val1 + val2
            case '-':
                return val1 - val2
            case 'x':
                return val1 * val2
            case '/':
                if (val2 == 0):
                    return 1
                return val1 / val2
            case 'sqr':
                return val1 * val1
            case 'sqrt':
                if (val1 >= 0):
                    return math.sqrt(val1)
                return 1
            case _:
                return 0
