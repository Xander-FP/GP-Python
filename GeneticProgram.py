import pandas
from random import Random
import GlobalVariables as global_vars
from random import random
from Creator import Creator
from Evaluator import Evaluator
from Trainer import Trainer
from Tester import Tester
from timeit import default_timer

class GeneticProgram:
    
    def __init__(self,seed ,file_path, population_size, max_depth, f_set, t_set, terminal_bound, t_size, grow_room, crossover_rate, bound):
        self.__df = pandas.read_csv(file_path,nrows=100)
        self.__splitData()
        self.__population_size = population_size
        self.__max_depth = max_depth
        self.evaluator = Evaluator()
        self.__grow_room = grow_room
        self.__bound = bound
        global_vars.function_set = f_set
        global_vars.terminal_set = t_set
        global_vars.num = Random(seed)
        global_vars.terminal_bound = terminal_bound
        global_vars.tournament_size = t_size
        global_vars.crossover_rate = crossover_rate

    def train(self, seed):
        creator = Creator()
        trainer = Trainer(self.__bound)
        programs = creator.generateInitialPop(self.__population_size, self.__max_depth)
        return trainer.train(self.__train_set,programs, self.__max_depth + self.__grow_room, seed) # Returns best program
    
    def test(self, program, seed):
        tester = Tester(self.__bound)
        tester.test(self.__test_set, program)
        print(seed, round(program.getHits()/len(self.__test_set),4)*100, '%')
        print(seed, program)

    def viewPopulation(self):
        for program in self.__programs:
            print(program)

    def __splitData(self):
        NUM = 7
        self.__train_set = []
        self.__train_set = self.__df[self.__df.index % NUM != 0]
        self.__test_set = self.__df[self.__df.index % NUM == 0]

    
