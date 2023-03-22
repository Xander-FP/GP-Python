from Evaluator import Evaluator
import GlobalVariables as global_vars 
from Node import Node
from Program import Program
import numpy as np
import gc
from timeit import default_timer

ITERATIONS = 200

class Trainer:

    def __init__(self, bound) -> None:
        self.__bound = bound
        self.__evaluator = Evaluator()

    # def evaluatePop(self,programs):
            # for i, row in self.__train_set.iterrows():
                
    
    def evaluatePop(self,row, programs):
        expected = row['Duration']
        for program in programs:
            val = 1
            val = self.__evaluator.evaluate(program, row)
            program.addFitness(round(abs(expected - val),2))
            if (round(expected - val,2) <= self.__bound):
                program.addHit()

    # def eval(self,program,expected,row):
    #     val = self.__evaluator.evaluate(program, row)
    #     program.addFitness(round(abs(expected - val),2))
    #     if (round(expected - val,2) <= self.__bound):
    #         program.addHit()
    #     return program

    def train(self, train_set, initial_pop, max_depth, seed, f):
        self.__train_set = train_set
        self.__max_depth = max_depth
        self.__pop = initial_pop

        # for i in range(ITERATIONS):
        count = 0
        converged = False
        prev:Program = None
        prev_matches = 0
        while count < ITERATIONS and not converged:
            work = default_timer()
            # self.evaluatePop(self.__pop)
            self.__train_set.apply(self.evaluatePop,1,args=(self.__pop,))
            work_end = default_timer() - work
            if (count%10 == 0 and count != 0):
                print('Count'+str(seed)+': ' + str(count) + ' -> ' + str(self.__best.getFitness()))
                print('evaluating', work_end)
                f.write(str(self.__best.getFitness()) + '\n')
                f.write(str(self.__best) + '\n')
            # print(i,self.__getBest())
            self.__getBest()
            # print('\n' + str(self.__best.getFitness()) + '************************************************************')
            self.__generateNewPop()
            gc.collect()

            count += 1
            if (prev == self.__best):
                prev_matches += 1
                if prev_matches >= 10:
                    converged = True
            else:
                prev_matches = 0
                prev = self.__best
        
        return self.__best

    def __getBest(self):
        self.__best = np.max(self.__pop)
        return self.__best

    def __generateNewPop(self):
        # Loop and generate children based on population
        new_pop = []
        crossover_count = int(len(self.__pop) * global_vars.crossover_rate)
        for i in range(0,crossover_count,2):
            new_pop.extend(self.__crossover())
        for i in range(len(self.__pop) - crossover_count):
            new_pop.append(self.__mutate())
        del(self.__pop)
        self.__pop = new_pop

    # Makes use of tournament selection to choose a parent
    def __selectParent(self) -> Program:
        best: Program = None
        for i in range(global_vars.tournament_size):
            parent = self.__pop[global_vars.num.randrange(len(self.__pop))]
            if (best == None or parent.getFitness() < best.getFitness()):
                best = parent
            else:
                if (parent.getFitness() == best.getFitness):
                    if (best.getHits() < parent.getHits()):
                        best = parent
        best.calcNumChildren()
        return best

    def __crossover(self):
        # Get the parents and get the nodes to swap
        parent_program1 = self.__selectParent()
        parent_program2 = self.__selectParent()
        new_program1 = parent_program1.clone()
        new_program2 = parent_program2.clone()
        pos1 = global_vars.num.randrange(new_program1.getHead().getNumChildren())
        if pos1 == 0:
            pos1 = 1
        pos2 = global_vars.num.randrange(new_program2.getHead().getNumChildren())
        if pos2 == 0:
            pos2 = 1
        self.__current_pos = 0
        node1 = self.__findNode(pos1,new_program1.getHead())
        self.__current_pos = 0
        node2 = self.__findNode(pos2,new_program2.getHead())
        
        # Make the swap
        temp_children = node1.getChildren()
        node1.setChildren(node2.getChildren())
        node2.setChildren(temp_children)
        temp_val = node1.getVal()
        node1.setVal(node2.getVal())
        node2.setVal(temp_val)
        new_program1.prune(self.__max_depth)
        new_program2.prune(self.__max_depth)
        return [new_program1, new_program2]

    def __mutate(self) -> Program:
        # Select mutation point
        parent = self.__selectParent()
        new_program = parent.clone()
        pos = global_vars.num.randrange(new_program.getHead().getNumChildren())
        if pos == 0:
            pos = 1
        self.__current_pos = 0
        node = self.__findNode(pos, new_program.getHead())
        # Mutate 
        node.setChildren([])
        node.mutate(self.__max_depth)
        new_program.prune(self.__max_depth)
        return new_program

    def __findNode(self, goal_pos, node: Node) -> Node:
        if (self.__current_pos == goal_pos):
            return node
        for child in node.getChildren():
            self.__current_pos += 1
            result = self.__findNode( goal_pos, child)
            if result != None:
                return result
        return None