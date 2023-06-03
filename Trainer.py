from Evaluator import Evaluator
import GlobalVariables as global_vars 
from Node import Node
from Program import Program
from Chromosome import Chromosome, Codon, generateProgram
import numpy as np
from timeit import default_timer

class Trainer:

    def __init__(self) -> None:
        self.__evaluator = Evaluator()

    def train(self, train_set, initial_pop, seed, f, max_grammar, generations):
        self.__train_set = train_set
        self.__pop = initial_pop
        self.__max_grammar = max_grammar
        count = 0
        converged = False
        prev:Chromosome = None
        prev_matches = 0
        while count < generations and not converged:
            # print the population
            for chromosome in self.__pop:
                print(chromosome)
            work = default_timer()
            self.__evaluatePop(self.__pop)
            work_end = default_timer() - work
            if (count%10 == 0 and count != 0):
                print('Count'+str(seed)+': ' + str(count) + ' -> ' + str(self.__best.getFitness()))
                print('evaluating', work_end)
                f.write('fitness: ' + str(self.__best.getFitness()) + '\n')
                f.write(str(self.__best) + '\n')
            self.__getBest()
            # print('\n' + str(self.__best.getFitness()) + '************************************************************')
            self.__generateNewPop()

            # Check for convergence
            count += 1
            if (prev == self.__best):
                prev_matches += 1
                if prev_matches >= 15:
                    # f.write(str(self.__best) + '\n')
                    f.write('converged')
                    f.write('fitness: ' + str(self.__best.getFitness()) + '\n')
                    converged = True
                    print('converged')
            else:
                prev_matches = 0
                prev = self.__best
        
        return self.__best
    
    def __evaluatePop(self,pop):
        programs = []
        # Convert the chromosomes to programs
        for chromosome in pop:
            program = generateProgram(self.__max_grammar,chromosome)
            programs.append(program)
        # Evaluate the programs
        for row in self.__train_set.itertuples():
            self.evaluate(row, programs)
        # Set the fitness of the chromosomes
        for i in range(len(pop)):
            pop[i].setFitness(programs[i].getFitness())

    def evaluate(self,row, programs):
        expected = getattr(row,'Duration')
        for program in programs:
            predicted = self.__evaluator.evaluate(program, row)
            program.addFitness(abs(expected - predicted))

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
    def __selectParent(self) -> Chromosome:
        best: Chromosome = None
        for i in range(global_vars.tournament_size):
            parent = self.__pop[global_vars.num.randrange(len(self.__pop))]
            if (best == None or parent.getFitness() < best.getFitness()):
                best = parent
        # best.calcNumChildren()
        return best

    def __crossover(self) -> list[Chromosome, Chromosome]:
        # Get the parents and get the nodes to swap
        parent_chromosome1 = self.__selectParent()
        parent_chromosome2 = self.__selectParent()
        new_chromosome1 = parent_chromosome1.clone()
        new_chromosome2 = parent_chromosome2.clone()
        pos1 = self.__selectCodon(new_chromosome1.getNumCodons())
        pos2 = self.__selectCodon(new_chromosome2.getNumCodons())

        # Swap parts of the chromosomes
        temp = new_chromosome1.getChromosome()[pos1]
        new_chromosome1.getChromosome()[pos1] = new_chromosome2.getChromosome()[pos2]
        new_chromosome2.getChromosome()[pos2] = temp

        # print('crossover')
        # print(parent_chromosome1)
        # print(parent_chromosome2)
        # print(pos1, pos2)
        # print('----------------')
        # print(new_chromosome1)
        # print(new_chromosome2)
        # print('################')

        return [new_chromosome1, new_chromosome2]
        
    def __mutate(self) -> Chromosome:
        # Select mutation point
        parent = self.__selectParent()
        new_program = parent.clone()
        pos = self.__selectCodon(new_program.getNumCodons())

        # Mutate a random codon
        new_program.getChromosome()[pos] = Codon()

        # print('mutate')
        # print(parent)
        # print(pos)
        # print('----------------')
        # print(new_program)
        # print('################')

        return new_program

    def __selectCodon(self, num_codons) -> int:
        return global_vars.num.randrange(num_codons)
    
    def __printList(self, list: list) -> None:
        out = '['
        for l in list:
            out += str(l) + ', '
        out += ']'
        print(out)