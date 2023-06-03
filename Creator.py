# Record num,Duration,Distance,PLong,PLatd,DLong,DLatd,Haversine,Pmonth,Pday,Phour,Pmin,PDweek,Dmonth,Dday,Dhour,Dmin,DDweek,Temp,Precip,Wind,Humid,Solar,Snow,GroundTemp,Dust
from Chromosome import Chromosome
import numpy as np

class Creator:

    def generateInitialPop(self, population_size, max_codons):
        population = np.empty(population_size, dtype=Chromosome)
        for i in range(population_size):
            population[i] = Chromosome()
            population[i].createChromosome(max_codons)
        return population
    