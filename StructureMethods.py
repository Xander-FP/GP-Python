import GlobalVariables as global_vars
from Program import Program

def isGlobalExplored(program:Program):
    for optima in global_vars.local_optima:
        if program.calculateSimilarity(optima) > global_vars.g_thresh:
            return True
    return False