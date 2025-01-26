import math

class FitnessFunction:
    def calculate(self, x):
        return math.log(abs(x**3)) * math.cos(x) * math.sin(x)

    #def calculate(self, x):
    #    return 0.1 * x * math.log(1 + abs(x)) * math.cos(x) ** 2
