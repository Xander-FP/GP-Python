# Record num,Duration,Distance,PLong,PLatd,DLong,DLatd,Haversine,Pmonth,Pday,Phour,Pmin,PDweek,Dmonth,Dday,Dhour,Dmin,DDweek,Temp,Precip,Wind,Humid,Solar,Snow,GroundTemp,Dust
from Program import Program
import numpy as np

class Creator:

    def generateInitialPop(self, population_size, max_depth):
        programs = np.empty(population_size,dtype=Program)
        for i in range(population_size):
            programs[i] = Program(max_depth)
        return programs
