from GeneticProgram import GeneticProgram
from timeit import default_timer
import loky
import multiprocessing


FILE_PATH = '../Data/gtfh9z865f-1/For_modeling.csv'
POPULATION_SIZE = 100
MAX_DEPTH = 4
FUNCTION_SET = ['+','-','*','/'] #,'sqrt','sqr'
TERMINAL_SET = ['Distance','PLong','PLatd','DLong','DLatd','Haversine','Pmonth','Pday','Phour','Pmin','PDweek','Dmonth','Dday','Dhour','Dmin','DDweek','Temp','Precip','Wind','Humid','Solar','Snow','GroundTemp','Dust']
TERMINAL_BOUND = 0.8
TOURNAMENT_SIZE = 5
GROW_ROOM = 3
CROSSOVER_RATE = 0.5
TRAINING_SET_SIZE = 0.7
BOUND = 0.01

def main(seed):
    gp = GeneticProgram(seed, FILE_PATH, POPULATION_SIZE, MAX_DEPTH, FUNCTION_SET, TERMINAL_SET, TERMINAL_BOUND, TOURNAMENT_SIZE, GROW_ROOM, CROSSOVER_RATE, BOUND)
    start = default_timer()
    best = gp.train(seed)
    duration = default_timer() - start
    print(seed, ':', duration)
    # gp.viewPopulation()
    gp.test(best, seed)

main(4)

# if __name__ == "__main__":
# #     # creating processes
#     p = []
#     for i in range(10):
#         p.append(multiprocessing.Process(target=main, args=(i,)))
  
#     for process in p:
#         process.start()

#     for process in p:
#         process.join()

#     print("DONE!")