from utils import Dique, Ship, Table, Queue, minium, size_values, \
    probability_sizes
from generator import DisGen, NorGen, ExpGen
# todo no se si halla problema con la numerica de los generadores ya que son
#  flotantes

# region initializer

queue = Queue()
# se crean las variables contadoras y de tiempo, y las demas que haran falta
time = 0
ship_counter = 1 # numero del proximo barco a arrivar
exited_ships = [] # los barcos que salieron

diques = [Dique(index) for index in range(5)] # los diques

events = {}
# inicialmente todos los tiempos son inf
events.update({f't{index}e': None for index in range(5)})
events.update({f't{index}t': None for index in range(5)})
events.update({f't{index}f': None for index in range(5)})
events.update({f't{index}s': None for index in range(5)})
# se setea el tiempo final, notar que en to_do momento trabajamos con minutos
# en caso de que se desee saber la hora se puede usar la funcion
# number_at_interval definida en utils

events['T'] = 60 * 12 # todo en minutos de 8 am a 8 pm
# se crea el proximo barco, el tamano es una discreta entre 1, 2, 4
ship = Ship(ship_counter, DisGen.generate(size_values, probability_sizes))
# se crea el primer evento de arribo del barco que vendra
events['ta'] = time + NorGen.generate(*Table.get_normal_params(ship.size, time))

# endregion
# mientras el puerto no halla cerrado o aun queden diques trabajando
while (events['T'] is not None and time <= events['T']) or \
        not all([dique.is_waiting for dique in diques]):

    mini = minium(events) # busca el menor tiempo
    # evento de arribo
    if mini[0] == 'ta':
        time = events['ta']
        ship.time.append(mini) # se le pone al barco un ticket con el tiempo de
        # entrada

        queue.add(ship)
        # se agrega el barco a la cola
        ship_counter += 1
        ship = Ship(ship_counter, DisGen.generate(size_values,
                                                  probability_sizes))
        # se crea el proximo barco que va a venir y se genera el tiempo de
        # arribo
        events['ta'] = time + NorGen.generate(
            *Table.get_normal_params(ship.size, time))
        # si el primer dique esta sin hacer nada genero la exponencial para
        # ponerlo a trabajar
        if diques[0].is_waiting:
            events['t0e'] = time + ExpGen.generate(4)

            diques[0].is_waiting = False

    elif mini[0] == 't0e':
        time = events['t0e']
        # se abrio la puerta del dique, entro los barcos y espero a que se
        # acomoden para echarle agua al dique
        events['t0e'] = None

        diques[0].add(queue.select(6))

        events['t0t'] = time + ExpGen.generate_times(2, len(diques[0].ships))

    elif mini[0] == 't0t':
        time = events['t0t']
        events['t0t'] = None
        # le echo agua al dique y espero a que se llene
        events['t0f'] = time + ExpGen.generate(7)

    elif mini[0] == 't0f':
        time = events['t0f']
        # si el otro dique esta sin hacer nada, le digo que habra la puerta
        # si el otro esta trabajando yo espero
        events['t0f'] = None

        if diques[1].is_waiting:
            events['t1e'] = time + ExpGen.generate(4)
            diques[1].is_waiting = False

        else: diques[0].freeze()

    elif mini[0] == 't0s':
        time = events['t0s']
        # si se produce una salida es porque el otro dique abrio su compuerta
        # y los barcos salieron, genero el tiempo en el que se llena el otro
        # diqe y si tengo barcos en la cola abro mi compuerta sino me quedo
        # sin hacer nada
        events['t0s'] = None

        events['t1t'] = time + ExpGen.generate_times(2, len(diques[1].ships))

        if queue.have_ships:
            events['t0e'] = time + ExpGen.generate(4)

        else: diques[0].is_waiting = True

    elif mini[0] == 't1e':
        time = events['t1e']
        events['t1e'] = None
        # abri mi compuerta saco los barcos del dique anterior a mi, si estaba
        # congelado lo descongelo y genero el tiempo en el que se van a demorar
        # en salir sus barcos
        diques[1].add(diques[0].unpack())

        if diques[0].frozen: diques[0].unfreeze()

        events['t0s'] = time + ExpGen.generate_times(1.5, len(diques[1].ships))

    elif mini[0] == 't1t':
        time = events['t1t']
        events['t1t'] = None

        events['t1f'] = time + ExpGen.generate(7)

    elif mini[0] == 't1f':
        time = events['t1f']
        events['t1f'] = None

        if diques[2].is_waiting:
            events['t2e'] = time + ExpGen.generate(4)
            diques[2].is_waiting = False

        else: diques[1].freeze()

    elif mini[0] == 't1s':
        time = events['t1s']
        events['t1s'] = None

        events['t2t'] = time + ExpGen.generate_times(2, len(diques[2].ships))

        if diques[0].frozen: events['t1e'] = time + ExpGen.generate(4)

        else: diques[1].is_waiting = True

    elif mini[0] == 't2e':
        time = events['t2e']
        events['t2e'] = None

        diques[2].add(diques[1].unpack())

        if diques[1].frozen: diques[1].unfreeze()

        events['t1s'] = time + ExpGen.generate_times(1.5, len(diques[2].ships))

    elif mini[0] == 't2t':
        time = events['t2t']
        events['t2t'] = None

        events['t2f'] = time + ExpGen.generate(7)

    elif mini[0] == 't2f':
        time = events['t2f']
        events['t2f'] = None

        if diques[3].is_waiting:
            events['t3e'] = time + ExpGen.generate(4)
            diques[3].is_waiting = False

        else: diques[2].freeze()

    elif mini[0] == 't2s':
        time = events['t2s']
        events['t2s'] = None

        events['t3t'] = time + ExpGen.generate_times(2, len(diques[3].ships))

        if diques[1].frozen:
            events['t2e'] = time + ExpGen.generate(4)

        else: diques[2].is_waiting = True

    elif mini[0] == 't3e':
        time = events['t3e']
        events['t3e'] = None

        diques[3].add(diques[2].unpack())

        if diques[2].frozen: diques[2].unfreeze()

        events['t2s'] = time + ExpGen.generate_times(1.5, len(diques[3].ships))

    elif mini[0] == 't3t':
        time = events['t3t']
        events['t3t'] = None

        events['t3f'] = time + ExpGen.generate(7)

    elif mini[0] == 't3f':
        time = events['t3f']
        events['t3f'] = None

        if diques[4].is_waiting:
            events['t4e'] = time + ExpGen.generate(4)
            diques[4].is_waiting = False

        else: diques[3].freeze()

    elif mini[0] == 't3s':
        time = events['t3s']
        events['t3s'] = None

        events['t4t'] = time + ExpGen.generate_times(2, len(diques[4].ships))

        if diques[2].frozen: events['t3e'] = time + ExpGen.generate(4)

        else: diques[3].is_waiting = True

    elif mini[0] == 't4e':
        time = events['t4e']
        events['t4e'] = None

        diques[4].add(diques[3].unpack())

        if diques[3].frozen: diques[3].unfreeze()

        events['t3s'] = time + ExpGen.generate_times(1.5, len(diques[4].ships))

    elif mini[0] == 't4t':
        time = events['t4t']
        events['t4t'] = None

        events['t4f'] = time + ExpGen.generate(7)

    elif mini[0] == 't4f':
        time = events['t4f']
        events['t4f'] = None

        events['t4s'] = time + ExpGen.generate_times(1.5, len(diques[4].ships))

        # se le agrega a cada barco el tiempo en el que salio
        for a_ship in diques[4].ships:
            a_ship.time.append(mini)
        # todos los barcos que pasaron por el canal se guardan
        exited_ships.extend(diques[4].unpack())

    elif mini[0] == 't4s':
        time = events['t4s']
        events['t4s'] = None

        if diques[3].frozen: events['t4e'] = time + ExpGen.generate(4)

        else: diques[4].is_waiting = True

    elif mini[0] == 'T':
        time = events['T']
        events['T'] = None

        events['ta'] = None

        queue.clear()

        if events['t0e'] is not None:
            events['t0e'] = None

            diques[0].is_waiting = True


# calculando el promedio de tiempo de espera de los barcos que salieron, por
# tiempo de espera entiendo el tiempo que se pasaron en el canal, se le resta
# al tiempo en el que salieron el tiempo en el que entraron y se divide toda esa
# suma con la cantidad de barcos que salieron que estan en una lista en ships
max_time = 0
for a_ship in exited_ships:
    max_time += (a_ship.time[1][1] - a_ship.time[0][1])

print(len(exited_ships))
print(max_time)






