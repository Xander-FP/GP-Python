from Evaluator import Evaluator

class Tester:

    def __init__(self, bound) -> None:
        self.__bound = bound
        self.__evaluator = Evaluator()

    def test(self, test_set, program):
        # print('***********Testing**************')
        program.resetHits()
        # print(program.getHits())
        for i, row in test_set.iterrows():
            expected = row['Duration']
            val = self.__evaluator.evaluate(program, row)
            if (round(expected - val,2) <= self.__bound):
                program.addHit()