from random import random
from math import log, cos, pi, sqrt
from utils import number_at_interval


class ExpGen:
    '''
    genera la exponencial
    '''
    @staticmethod
    def generate(l):
        # l = 1 / l
        return -(log(random()) / l)

    @staticmethod
    def generate_times(l, times):
        '''
        genera exponenciales times veces con lambda l y devuelve la suma de las
        mismas
        :param l: lambda de la funcion
        :type l: float
        :param times: cantidad de veces a generar
        :type times: int
        :return: suma de las variables generadas
        :rtype: float
        '''
        result = 0

        for index in range(times):
            result += ExpGen.generate(l)

        return result


class NorGen:
    '''
    genera la normal
    '''
    @staticmethod
    def generate(median, sigma):
        result = -1
        while result < 0:
            result = sqrt(-2.0 * log(random())) * cos(2.0 * pi * random())

        return result * sqrt(sigma) + median


class DisGen:
    '''
    genera una variable aleatorio discreta
    '''
    @staticmethod
    def generate(value, probability):
        assert len(value) - 1 == len(probability)
        assert all([isinstance(integer, int) for integer in value])
        assert all([isinstance(integer, float) for integer in probability])

        return number_at_interval(value, probability, random(), 0)


if __name__ == '__main__':

    for times in range(10000):
        print(ExpGen.generate(1.5))
