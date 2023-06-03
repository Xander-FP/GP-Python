from Evaluator import Evaluator
import math
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score as r_2
from sklearn.metrics import median_absolute_error as medae
from sklearn.metrics import mean_absolute_error as mae
from Chromosome import generateProgram


class Tester:

    def __init__(self) -> None:
        self.__evaluator = Evaluator()

    def test(self, test_set, chromosome, max_grammar):
        program = generateProgram(max_grammar,chromosome)
        # print('***********Testing**************')
        expected = []
        predicted = []
        for row in test_set.itertuples():
            expt = getattr(row,'Duration')
            expected.append(expt)
            pred = round(self.__evaluator.evaluate(program, row))
            predicted.append(pred)
        # print(str(seed) + ':' + str((program.getHits()/len(test_set)) * 100) + ' %')
        return (predicted, expected)


    def RMSE(self, predicted, expected):
        return math.sqrt(mse(expected, predicted))

    def R_Squared(self, predicted, expected):
        return r_2(expected, predicted)

    def MedAE(self, predicted, expected):
        return medae(expected, predicted)

    def MAE(self, predicted, expected):
        return mae(expected, predicted)