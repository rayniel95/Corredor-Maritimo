from typing import List


size_values = (1, 2, 4)
probability_sizes = (0.33, 0.66)


class Ship:

    def __init__(self, id, size):
        assert size in (1, 2, 4,)
        self.id = id
        self.size = size
        self.time = [] # para guardar los distintos tiempos


class Dique:

    def __init__(self, id):
        self.is_waiting = True
        self._ships = []
        self.id = id
        self.frozen = False

    @property
    def is_waiting(self):
        return self._is_waiting

    @is_waiting.setter
    def is_waiting(self, value):
        assert isinstance(value, bool)
        self._is_waiting = value

    def add(self, ships):
        self._ships = ships

    @property
    def ships(self):
        return self._ships

    @ships.setter
    def ships(self, value):
        self._ships = value

    # region Frozeen methods and attr

    @property
    def frozen(self):
        return self._freeze

    @frozen.setter
    def frozen(self, value):
        self._freeze = value

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    # endregion

    def unpack(self):
        result = [ship for ship in self.ships]
        self.ships.clear()
        return result


class Queue:

    def __init__(self):
        self._queue = []

    def select(self, sum_size):
        '''
        selecciona la cantidad de barcos de forma consecutiva tal que la suma de
        sus pesos sea menor o igual que sum_size, para que quepan en el canal
        :param sum_size: la suma del peso de los barcos seleccionados de la cola
        :type sum_size: int
        :return: los barcos seleccionado de forma secuencial tal que la suma de
        sus pesos sea menor o igual que sum_size
        :rtype: List[Ship]
        '''
        result = []
        size = 0

        for ship in self._queue:
            if ship.size + size <= sum_size:
                size += ship.size
                result.append(ship)

        for element in result:
            self._queue.remove(element)

        return result

    def add(self, ship):
        self._queue.append(ship)

    @property
    def have_ships(self):
        return len(self._queue) > 0

    def clear(self):
        self._queue.clear()


class Table:

    @staticmethod
    def get_normal_params(ship_size, t):
        result = number_at_interval([((5, 2,), (15, 3,), (45, 3,),),
                                     ((3, 1,), (10, 5,), (35, 7,),),
                                     ((10, 2,), (20, 5,), (60, 9,),)],
                                    [180, 540], t, 0)

        if ship_size == 1: return result[0]
        if ship_size == 2: return result[1]

        return result[2]


def number_at_interval(values, intervals, number, lower_bound):
    '''
    dada una lista values y las divisiones de un intervalo numerico y un numero
    que pertenece a dicho intervalo, donde lower_bound es el inicio del
    intervalo y no se pone el final del mismo, devuelve el primer valor de la
    lista values si lower_bound <= numero < intervals[0], devuelve el segundo
    si intervals[0] <= number < intervals[1], etc, sino devuelve el ultimo
    :param values:
    :type values:
    :param intervals:
    :type intervals:
    :param number:
    :type number:
    :param lower_bound:
    :type lower_bound:
    :return:
    :rtype:
    '''
    for index in range(len(intervals)):
        if lower_bound <= number < intervals[index]:
            return values[index]

        lower_bound = intervals[index]

    return values[-1]


def minium(event_dict):
    my_list = list(event_dict.items())

    mini = my_list[0]

    for element in my_list:
        if mini[1] is None or (element[1] is not None and element[1] < mini[1]):
            mini = element

    return mini


if __name__ == '__main__':
    events = {1: None, 2: 3, 4: 5}

    print(minium(events))
