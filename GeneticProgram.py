import pandas
from random import Random
import GlobalVariables as global_vars
from Creator import Creator
from Trainer import Trainer
from Tester import Tester

class GeneticProgram:
    
    def __init__(self,seed ,file_path, population_size, max_depth, f_set, t_set, terminal_bound, t_size, grow_room, crossover_rate, g_thresh, l_thresh):
        self.__df = pandas.read_csv(file_path,nrows=100000)
        self.__splitData()
        self.__population_size = population_size
        self.__max_depth = max_depth
        self.__grow_room = grow_room
        global_vars.function_set = f_set
        global_vars.terminal_set = t_set
        global_vars.num = Random(seed)
        global_vars.terminal_bound = terminal_bound
        global_vars.tournament_size = t_size
        global_vars.crossover_rate = crossover_rate
        global_vars.local_optima = set()
        global_vars.g_thresh = g_thresh
        global_vars.l_thresh = l_thresh

    def train(self, seed, f, G_ITER):
        # Initialize 
        creator = Creator()
        trainer = Trainer()
        tester = Tester()

        # Global search for ISBA
        for i in range(G_ITER):
            programs = creator.generateInitialPop(self.__population_size, self.__max_depth)
            program = trainer.train(self.__train_set,programs, self.__max_depth + self.__grow_room, seed, f)
            global_vars.local_optima.add(program)

        # Local search for ISBA
        
        # Pass through all the local optima for testing
        print('Starting getting training accuracy for ' + str(seed))
        for optimum in global_vars.local_optima:
            results = tester.test(self.__train_set, optimum, seed)
            self.__writeResults(f, seed, predicted = results[0], expected = results[1], tester = tester)
        return global_vars.local_optima
    
    def test(self, optima, seed, f):
        tester = Tester()
        best = None
        for optimum in optima:
            results = tester.test(self.__test_set, optimum, seed)
            temp = tester.RMSE(results[0],results[1])
            if best == None or best > temp:
                best = temp
            self.__writeResults(f, seed, predicted = results[0], expected = results[1], tester = tester)
        print(str(seed) + ': ' + str(best))
        


    def viewPopulation(self):
        for program in self.__programs:
            print(program)

    def __splitData(self):
        self.__df['Distance'] = self.__df['Distance'].map(lambda x: x/1000)
        NUM = 7
        self.__train_set = self.__df[self.__df.index % NUM != 0]
        self.__test_set = self.__df[self.__df.index % NUM == 0]

    def __writeResults(self, f, seed, predicted, expected, tester):
        f.write('\nSeed: ' + str(seed) + '--RMSE-->' + str(tester.RMSE(predicted, expected)) + '\n')
        f.write('Seed: ' + str(seed) + '--R_Squared-->'+ str(tester.R_Squared(predicted, expected))+ '\n')
        f.write('Seed: ' + str(seed) + '--MedAE-->'+ str(tester.MedAE(predicted, expected))+ '\n')
        f.write('Seed: ' + str(seed) + '--MAE-->'+ str(tester.MAE(predicted, expected))+ '\n')

    
