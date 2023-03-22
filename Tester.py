from Evaluator import Evaluator
import pandas
import numpy as np
from sklearn.metrics import mean_squared_error as rmse
from sklearn.metrics import r2_score as r_2
from sklearn.metrics import median_absolute_error as medae
from sklearn.metrics import mean_absolute_error as mae


class Tester:

    def __init__(self, bound) -> None:
        self.__bound = bound
        self.__evaluator = Evaluator()

    def test(self, test_set, program):
        # print('***********Testing**************')
        program.resetHits()
        expected = []
        predicted = []
        for i, row in test_set.iterrows():
            expected.append(row['Duration'])
            predicted.append(round(self.__evaluator.evaluate(program, row)))
        return (predicted, expected)


    def RMSE(self, predicted, expected):
        return rmse(expected, predicted)

    def R_Squared(self, predicted, expected):
        return r_2(expected, predicted)

    def MedAE(self, predicted, expected):
        return medae(expected, predicted)

    def MAE(self, predicted, expected):
        return mae(expected, predicted)