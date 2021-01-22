from typing import Tuple, List

size_values = Tuple[int, int, int]
probability_sizes = Tuple[float, float]

# todo terminar los pyi si me da tiempo
class Ship:

    id:int
    size: int
    time: List[Tuple[str, float]]

    def __init__(self, id: int, size: int): ...


class Dique:

    _ships: List[Ship]
    id:int
    frozen: bool
    _is_waiting: bool

    def __init__(self, id: int): ...

    @property
    def is_waiting(self) -> _is_waiting: ...

    @is_waiting.setter
    def is_waiting(self, value: bool): ...

    def add(self, ships: List[Ship]): ...

    @property
    def ships(self) -> _ships: ...

    @ships.setter
    def ships(self, value: List[Ship]): ...

    # region Frozeen methods and attr

    @property
    def frozen(self) -> bool: ...

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

    for index in range(len(intervals)):
        if lower_bound <= number < intervals[index]:
            return values[index]

        lower_bound = intervals[index]

    return values[-1]


def minium(event_dict: dict):
    my_list = list(event_dict.items())

    mini = my_list[0]

    for element in my_list:
        if mini[1] is None or (element[1] is not None and element[1] < mini[1]):
            mini = element

    return mini


