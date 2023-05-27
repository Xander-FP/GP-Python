from Evaluator import Evaluator
import GlobalVariables as global_vars 
from Node import Node
from Program import Program
import numpy as np
from timeit import default_timer
import StructureMethods as Structure

ITERATIONS = 250

class Trainer:

    def __init__(self) -> None:
        self.__evaluator = Evaluator()

    def evaluatePop(self,pop):
        for row in self.__train_set.itertuples():
            self.evaluate(row, pop)
                
    def evaluate(self,row, programs):
        expected = getattr(row,'Duration')
        for program in programs:
            predicted = self.__evaluator.evaluate(program, row)
            program.addFitness(abs(expected - predicted))

    def global_search(self, train_set, initial_pop, max_depth,seed, f):
        pass

    def local_search(self, train_set, initial_pop, max_depth,seed, f):
        pass

    def train(self, train_set, initial_pop, max_depth,seed, f):
        # Initialize class variables
        self.__train_set = train_set
        self.__max_depth = max_depth
        self.__pop = initial_pop
        generation = 0

        # To check if converged 
        converged = False
        prev:Program = None
        prev_matches = 0

        while generation < ITERATIONS and not converged:
            work = default_timer()
            self.evaluatePop(self.__pop)
            self.__getBest()
            self.__generateNewPop()
            work_end = default_timer() - work
            generation += 1
            if (generation%10 == 0):
                self.__logProgress(f,seed,generation,work_end)
            
            # Check if the GP has converged to a certain fitness
            if (prev == self.__best):
                prev_matches += 1
                if prev_matches >= 15:
                    f.write('fitness: ' + str(self.__best.getFitness()) + '\n hits: ' + str(self.__best.getHits()) + '\n')
                    # f.write(str(self.__best) + '\n')
                    converged = True
                    print('converged')
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
        best.calcNumChildren()
        return best

    def __crossover(self):
        # Get the parents and get the nodes to swap
        parent_program1 = self.__selectParent()
        parent_program2 = self.__selectParent()
        while True:
            new_program1 = parent_program1.clone()
            new_program2 = parent_program2.clone()
            pos1 = self.__getPos(new_program1.getHead().getNumChildren())
            pos2 = self.__getPos(new_program2.getHead().getNumChildren())
            self.__current_pos = 0
            node1, index1 = self.__findNode(pos1,new_program1.getHead(),0)
            self.__current_pos = 0
            node2, index2 = self.__findNode(pos2,new_program2.getHead(),0)
            
            # Make the swap
            # If both trees are at the root then swapping them will have no effect
            if node1.getParent() == None and node2.getParent() == None:
                return [new_program1, new_program2]
            elif node1.getParent() == None:
                parent2 = node2.getParent()
                parent2.getChildren()[index2] = node1
                new_program1.setHead(node2)
                node1.setParent(parent2)
                node2.setParent(None)
            elif node2.getParent() == None:
                parent1 = node1.getParent()
                parent1.getChildren()[index1] = node2
                new_program2.setHead(node1)
                node1.setParent(None)
                node2.setParent(parent1)
            else:
                parent1 = node1.getParent()
                parent2 = node2.getParent()
                parent1.getChildren()[index1] = node2
                parent2.getChildren()[index2] = node1
                node1.setParent(parent2)
                node2.setParent(parent1)
                if not (Structure.isGlobalExplored(new_program1) or Structure.isGlobalExplored(new_program2)):
                    break

        new_program1.prune(self.__max_depth)
        new_program2.prune(self.__max_depth)
        return [new_program1, new_program2]

    def __mutate(self) -> Program:
        parent_program = self.__selectParent()
        # Mutate until the structure is not the same; 
        # Reset to unmutated program 
        while True:
            # Select mutation point
            new_program = parent_program.clone()
            pos = self.__getPos(new_program.getHead().getNumChildren())
            self.__current_pos = 0
            node, index = self.__findNode(pos, new_program.getHead(),0)

            # perform mutation
            if node.getParent() == None:
                new_node = Node.generateNode(None)
                new_program.setHead(new_node)
            else:
                parent = node.getParent()
                new_node = Node.generateNode(parent)
                parent.getChildren()[index] = new_node
            new_node.generate(self.__max_depth)
            if not Structure.isGlobalExplored(new_program):
                break
        
        return new_program
    
    def __findNode(self, goal_pos: int, node: Node, index: int) -> Node:
        if (self.__current_pos == goal_pos):
            return (node, index)
        children = node.getChildren()
        for i in range(len(children)):
            child = children[i]
            self.__current_pos += 1
            result = self.__findNode(goal_pos, child, i)
            if result != None:
                return result
        return None
    
    def __logProgress(self, f, seed, generation, time = 0):
        print('Generation('+str(seed)+'): ' + str(generation) + ' -> ' + str(self.__best.getFitness()))
        print('Time('+str(seed) + '):' + str(time))
        f.write('Raw Fitness: ' + str(self.__best.getFitness()) + '\n')
        f.write(str(self.__best) + '\n')

    def __getPos(self, num_children):
        # Check if equal to 0 because global_vars.num.randrange cannot accept 0 as a parameter
        if num_children == 0:
            return 0
        else:
            return global_vars.num.randrange(num_children)