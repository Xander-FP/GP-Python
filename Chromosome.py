import numpy as np
import GlobalVariables as global_vars
from Program import Program
from Node import Node
from NonTerminals import *
import math

class Chromosome:
    def __init__(self):
        self.__fitness = 0
        self.__num_codons = 0

    def getFitness(self):
        return self.__fitness
    
    def setFitness(self, fitness):
        self.__fitness = fitness

    def createChromosome(self, max_codons):
        # Create a numpy chromosome of Codon with a random number of codons
        num_codons = global_vars.num.randint(3, max_codons)
        self.__num_codons = num_codons
        self.__chromosome = np.empty(num_codons, dtype=Codon)
        for i in range(num_codons):
            self.__chromosome[i] = Codon()

    def getChromosome(self):
        return self.__chromosome
    
    def getDenaryChromosome(self):
        size = len(self.__chromosome)
        denary_chromosome = np.empty(size, dtype=int)
        for i in range(size):
            denary_chromosome[i] = self.__chromosome[i].getDenary()
        return denary_chromosome
    
    def getNumCodons(self):
        return self.__num_codons
    
    def clone(self):
        clone = Chromosome()
        clone.setFitness(self.__fitness)
        clone.__num_codons = self.__num_codons
        clone.__chromosome = np.copy(self.__chromosome)
        return clone
    
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
    
    def __str__(self) -> str:
        # Print out the chromosome as a string of codons
        return '|'.join(str(x) for x in self.__chromosome)


class Codon:
    def __init__(self):
        self._number_of_bits = 8
        self._codon = np.empty(self._number_of_bits, dtype=int)
        for i in range(self._number_of_bits):
            self._codon[i] = global_vars.num.randint(0, 1)

    def getDenary(self):
        denary = 0
        for i in range(self._number_of_bits):
            denary += self._codon[i] * 2 ** i
        return denary
    
    def __str__(self) -> str:
        # Print out the codon as a string of 1s and 0s
        return ''.join(str(x) for x in self._codon)
    
def generateProgram(max_grammar, chromosome: Chromosome) -> Program:
    denary = chromosome.getDenaryChromosome()
    program = Program()
    grammar:List[NonTerminal] = [Expr()]
    terminals = []
    count = 0
    codon_index = 0

    # Generate the terminals based on the grammar and the chromosome
    stopped = False
    while len(grammar) > 0:
        if count >= max_grammar:
            stopped = True
            break
        symbol = grammar.pop(0)
        part = symbol.applyRule(denary[codon_index%chromosome.getNumCodons()]%symbol.getNumRules())
        codon_index += 1
        if (isinstance(part[0], NonTerminal)):
            grammar.extend(part)
        else:
            terminals.extend(part)
        count += 1

    # self.__printList(terminals)
    # self.__printList(grammar)
    
    # Add the nodes to the program based on the terminals
    program.setHead(terminals.pop(0))
    currNode = program.getHead()
    if (stopped):
        program.addFitness(math.inf)
        return program
    __addChildren(currNode,terminals)
    return program

def __addChildren(currNode: Node, terminals: List[Node]) -> None:
    if (currNode.isTerminal()):
        return
    else:
        left = terminals.pop(0)
        left.__parent = currNode
        currNode.addChild(left)
        __addChildren(left, terminals)
        right = terminals.pop(0)
        right.__parent = currNode
        currNode.addChild(right)
        __addChildren(right, terminals)