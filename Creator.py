# Record num,Duration,Distance,PLong,PLatd,DLong,DLatd,Haversine,Pmonth,Pday,Phour,Pmin,PDweek,Dmonth,Dday,Dhour,Dmin,DDweek,Temp,Precip,Wind,Humid,Solar,Snow,GroundTemp,Dust
from Program import Program
import numpy as np
import StructureMethods as Structure

class Creator:

    def generateInitialPop(self, population_size, max_depth):
        programs = np.empty(population_size,dtype=Program)
        i = 0
        while i < population_size:
            program = Program(max_depth)
            if not Structure.isGlobalExplored(program):
                programs[i] = program
                i += 1
        return programs
