from Node import Node
import GlobalVariables as global_vars
import math
class Evaluator:

    def evaluate(self, program, data_set):
        # print('-------------------')
        # print(program.getFitness())
        # print(program)
        if (program.getFitness() == math.inf):
            return math.inf
        self.__data_set = data_set
        return self.__evaluate(program.getHead())

    # Recursive private function to evaluate the tree
    def __evaluate(self,current:Node):
        if(current.isTerminal()):
            return self.__getValue(current.getVal())
        children = current.getChildren()
        if (len(children) == 1):
            return current.performOperation(self.__evaluate(children[0]))
        return current.performOperation(self.__evaluate(children[0]), self.__evaluate(children[1]))
        
    def __getValue(self, item):
        if item == 'CONST':
            return global_vars.num.randrange(9)+1
        return getattr(self.__data_set,item)

