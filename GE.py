# Build programs using NonTerminal and Terminal nodes
import pandas
import GlobalVariables as global_vars
from Creator import Creator
from Trainer import Trainer
from Tester import Tester
from random import Random

class GE:
    def __init__(self,seed ,file_path, population_size, crossover_rate, num_generations, tournament_size, terminal_bound, max_grammar, max_codons,data_size):
        self.__df = pandas.read_csv(file_path,nrows=data_size)
        self.__splitData()
        self.__population_size = population_size
        self.__seed = seed
        self.__max_grammar = max_grammar
        self.__generations = num_generations
        global_vars.num = Random(seed)
        global_vars.crossover_rate = crossover_rate
        global_vars.tournament_size = tournament_size
        global_vars.terminal_bound = terminal_bound
        global_vars.max_codons = max_codons

    def train(self, f):
        creator = Creator()
        trainer = Trainer()
        tester = Tester()

        chromosomes = creator.generateInitialPop(self.__population_size, global_vars.max_codons)
        best = trainer.train(self.__train_set, chromosomes,self.__seed, f, self.__max_grammar,self.__generations)
        results = tester.test(self.__train_set, best, self.__max_grammar)
        f.write('\n Training Set: \n')
        self.__writeResults(f, results[0], results[1], tester)

        return best


    def test(self, best, f):
        tester = Tester()

        results = tester.test(self.__test_set, best, self.__max_grammar)
        f.write('\n Testing Set: \n')
        self.__writeResults(f, results[0], results[1], tester)

    def viewPopulation(self):
        pass

    def __splitData(self):
        self.__df['Distance'] = self.__df['Distance'].map(lambda x: x/1000)
        NUM = 7
        self.__train_set = self.__df[self.__df.index % NUM != 0]
        self.__test_set = self.__df[self.__df.index % NUM == 0]

    def __writeResults(self, f, predicted, expected, tester):
        f.write('Seed: ' + str(self.__seed) + '--RMSE-->' + str(tester.RMSE(predicted, expected)) + '\n')
        f.write('Seed: ' + str(self.__seed) + '--R_Squared-->'+ str(tester.R_Squared(predicted, expected))+ '\n')
        f.write('Seed: ' + str(self.__seed) + '--MedAE-->'+ str(tester.MedAE(predicted, expected))+ '\n')
        f.write('Seed: ' + str(self.__seed) + '--MAE-->'+ str(tester.MAE(predicted, expected))+ '\n')