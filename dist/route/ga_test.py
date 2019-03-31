from holland import Evolver
from holland.library import get_uniform_crossover_function
from holland.utils import bound_value
import random
import math




INPUT_ARRAY = [
    {"iotid": 25, "coords": (1, 2)},
    {"iotid": 21, "coords": (233, 122)},
    {"iotid": 23, "coords": (456, 345)},
    {"iotid": 28, "coords": (123, 43)},
    {"iotid": 27, "coords": (432, 231)},
    {"iotid": 29, "coords": (457, 764)},
    {"iotid": 26, "coords": (34, 243)},
    {"iotid": 24, "coords": (432, 465)},
    {"iotid": 22, "coords": (655, 844)},
    {"iotid": 210, "coords": (482, 342)},
    {"iotid": 20, "coords": (346, 1234)},
    {"iotid": 212, "coords": (431, 678)},
    {"iotid": 211, "coords": (835, 46)}
]

###############################
# GA Implementation
###############################

def distance(id_a, id_b):
    a = INPUT_ARRAY[id_a]['coords']
    b = INPUT_ARRAY[id_b]['coords']
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

def fitness_function(genome):
    total_dist = 0
    # Reject invalid
    if len(genome['path']) != len(set(genome['path'])):
        return math.inf
    for i in range(len(genome['path'])-1):
        total_dist = total_dist + distance(genome["path"][i], genome["path"][i+1])
    if total_dist < fitness_function.best_route_in_history_len:
        fitness_function.best_route_in_history_len = total_dist
        fitness_function.best_route_in_history = genome['path']
    return total_dist

fitness_function.best_route_in_history = []
fitness_function.best_route_in_history_len = math.inf

# init to random order
def init_distr():
    elem = random.choice(init_distr.curr_list)
    init_distr.curr_list.remove(elem)
    if len(init_distr.curr_list) == 0:
        init_distr.curr_list = [i for i in range(0, len(INPUT_ARRAY))]
    return elem
init_distr.curr_list = [i for i in range(0, len(INPUT_ARRAY))]

def swap(gene):
    ind1 = random.randint(0, len(gene)-1)
    ind2 = random.randint(0, len(gene)-1)
    temp = gene[ind2]
    gene[ind2] = gene[ind1]
    gene[ind1] = temp
    return gene

def pmx_randlen(genomes):
    i1 = random.randint(0,len(genomes[0])-1)
    i2 = len(genomes[0])-1 # random.randint(i1+2, len(genomes[0])-1)
    a = genomes[0]
    b = genomes[1]
    for i in range(i1, i2):
        swap_index = a.index(b[i])
        a[swap_index] = a[i]
        a[i] = b[i]
    return a

genome_params = {
    "path": {
        "type": "[int]",
        "size": len(INPUT_ARRAY),
        "possible_values": [i for i in range(len(INPUT_ARRAY))],
        "initial_distribution": init_distr,
        "mutation_function": swap,
        "mutation_level": "gene",
        "crossover_function": pmx_randlen,
        "mutation_rate": 0.1
    }
}

selection_strategy = {"pool": {"top": 10}}

# Run Evolution
evolver = Evolver(
    fitness_function,
    genome_params,
    selection_strategy,
    should_maximize_fitness=False
)

final_population = evolver.evolve(
            # generation_params={"n_elite": 3},
            # initial_population=[{"path": [1,2,3,4,5,6,7,8,9,0,10,11,12]}, {"path": [1,2,3,4,5,6,7,8,9,0,10,11,12]}],
            stop_conditions={"target_fitness": 0, "n_generations": 400},
            storage_options={},
            logging_options={'format': '%(message)s', 'level': 20})

with open("testout.txt", 'a') as fout:
    fout.write(str(fitness_function.best_route_in_history)
            + " :: " + str(fitness_function.best_route_in_history_len) + "\n")
