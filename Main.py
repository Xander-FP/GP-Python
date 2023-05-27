from GeneticProgram import GeneticProgram
from timeit import default_timer
import multiprocessing

FILE_PATH = './For_modeling.csv'
POPULATION_SIZE = 100
MAX_DEPTH = 3
FUNCTION_SET = ['+','-','*','/'] #,'sqrt','sqr'
TERMINAL_SET = ['Distance','Haversine','Wind','Snow','Precip','GroundTemp','Dust','Humid','Solar','Temp']#,'Pmonth','Pday','Phour','Pmin','PDweek','Dmonth','Dday','Dhour','Dmin','DDweek','PLong','PLatd','DLong','DLatd',
TERMINAL_BOUND = 0.5
TOURNAMENT_SIZE = 5
GROW_ROOM = 3
CROSSOVER_RATE = 0.7
TRAINING_SET_SIZE = 0.7
G_THRESH = 5
G_ITER = 4

def main(seed):
    with open(str(seed) + '.txt','w') as f:
        print('starting')
        gp = GeneticProgram(seed, FILE_PATH, POPULATION_SIZE, MAX_DEPTH, FUNCTION_SET, TERMINAL_SET, TERMINAL_BOUND, TOURNAMENT_SIZE, GROW_ROOM, CROSSOVER_RATE, G_THRESH, L_THRESH)
        best = gp.train(seed,f,G_ITER)
        gp.test(best, seed, f)

if __name__ == "__main__":
    start = default_timer()
    p = []
    for i in range(12):
        p.append(multiprocessing.Process(target=main, args=(i,)))
  
    for process in p:
        process.start()

    for process in p:
        process.join()

    duration = default_timer() - start
    print("DONE!")
    print("Duration:",duration)