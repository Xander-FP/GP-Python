from GE import GE
from timeit import default_timer
from NonTerminals import *
import multiprocessing

FILE_PATH = './For_modeling.csv'
POPULATION_SIZE = 100
TERMINAL_BOUND = 0.5
TOURNAMENT_SIZE = 5
CROSSOVER_RATE = 0.7
NUM_GENERATIONS = 100
MAX_GRAMMAR = 200 # The maximum ammount of times that a the codons of a chromosome can be used in a loop
MAX_CODONS = 10
DATA_SIZE = 1000

def main(seed):
    with open(str(seed) + '.txt','w') as f:
        print('starting')
        ge = GE(seed, FILE_PATH, POPULATION_SIZE, CROSSOVER_RATE, NUM_GENERATIONS, TOURNAMENT_SIZE, TERMINAL_BOUND, MAX_GRAMMAR, MAX_CODONS, DATA_SIZE)
        best = ge.train(f)
        ge.test(best, f)

if __name__ == "__main__":
    start = default_timer()
    p = []
    for i in range(1):
        p.append(multiprocessing.Process(target=main, args=(i,)))
  
    for process in p:
        process.start()

    for process in p:
        process.join()

    duration = default_timer() - start
    print("DONE!")
    print("Duration:",duration)