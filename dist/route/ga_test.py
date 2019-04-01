from holland import Evolver
from holland.library import get_uniform_crossover_function
from holland.utils import bound_value
import random
import math
import logging
import os
import pickle
import requests
import geopy.distance
import copy

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

INPUT_ARRAY = []
CREW_ARRAY = []

def CalcDist(bot_list, crew_list, routes):
    cb_dist = []
    for crew in crew_list:
        for bot in bot_list:
            dist = geopy.distance.distance(bot['coord'],crew['coord']).m
            cb_dist.append({'crewid': crew['iotid'], 'robotid': bot['iotid'], 'dist': dist, 'botcoord': bot['coord']})

    cb_dist = sorted(cb_dist, key=lambda k: k['dist'])
    min_len = math.inf
    for crew in crew_list:
        if len(crew['route']) < min_len:
            min_len = len(crew['route'])


    for route in cb_dist:
        for crew in crew_list:
            if (route['crewid'] == crew['iotid']) and (len(crew['route']) < (min_len*2+1)):
                crew['route'].append(route['robotid'])
                crew['coord'] = route['botcoord']
                bot_list = [bot for bot in bot_list if bot['iotid'] != route['robotid']]
                return bot_list
                break
        else:
            continue
        break



def main():
    """
    Crew data from monitor_out.data
    """
    with open('./monitor_out.data', 'rb') as fin:
        data_in = pickle.load(fin)
    crew_data = data_in["crew_list"]

    crew_list = []
    for crew in crew_data:
        crew_list.append({'iotid': crew})


    """
    Broken bots status data from monitor_out2.data
    """
    with open('./monitor_out2.data', 'rb') as fin:
        broken_bots = pickle.load(fin)

    broken_bots = [bot for bot in broken_bots if bot['status'] != 'Healthy']


    """
    Obtain coordinates of crew and broken robots
    Obtain crew description
    """
    crew_error = []

    for index in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")/Locations", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                if responseJSON['@iot.count'] == 0:
                    crew_error.append(index['iotid'])
                else:
                    index['coord'] = responseJSON['value'][0]['location']['coordinates']
                    index['route'] = []
            else:
                print("there was an error getting crew coordinate")
        except:
            logging.exception("Failed getting list of crew coordinates")

    crew_list = [crew for crew in crew_list if crew['iotid'] not in crew_error]


    for index in crew_list:
        try:
            crew_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")", headers = headers)
            if (crew_loc.status_code >= 200) and (crew_loc.status_code < 300):
                responseJSON = crew_loc.json()
                index['desc'] = responseJSON['description']
            else:
                print("there was an error getting crew description")
        except:
            logging.exception("Failed getting list of crew description")


    for index in broken_bots:
        try:
            broken_bot_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")/Locations", headers = headers)
            if (broken_bot_loc.status_code >= 200) and (broken_bot_loc.status_code < 300):
                responseJSON = broken_bot_loc.json()
                index['coord'] = responseJSON['value'][0]['location']['coordinates']
            else:
                print("there was an error getting coordinates for bots")
        except:
            logging.exception("Failed getting list of broken bots coordinates")


    """
    Swap coordinate format to [lat,long]
    """
    for crew in crew_list:
        lon, lat = crew['coord'][0], crew['coord'][1]
        crew['coord'] = lat, lon

    for bot in broken_bots:
        lon, lat = bot['coord'][0], bot['coord'][1]
        bot['coord'] = lat, lon

    for bot in broken_bots:
        INPUT_ARRAY.append(copy.deepcopy(bot))

    """
    If crew description is valid and not empty, add to crew route
    """
    for crew in crew_list:
        if not crew['desc']:
            continue
        else:
            crew_desc = crew['desc'][1:-1]
            crew_desc = crew_desc.split(',')
            try:
                crew_desc = list(map(int, crew_desc))
                crew['route'] = crew_desc
                for bot in broken_bots:
                    if crew_desc[-1] == bot['iotid']:
                        crew['coord'] = bot['coord']
                broken_bots = [bot for bot in broken_bots if bot['iotid'] not in crew_desc]
            except:
                crew['desc'] = [];

    for crew in crew_list:
        CREW_ARRAY.append(copy.deepcopy(crew))


    """
    Calculate distance between crew and robot
    """
    routes = []
    while broken_bots != []:
        broken_bots = CalcDist(broken_bots, crew_list, routes)


    """
    Updating 'Thing' description
    """
    for crew in crew_list:
        if not crew['route']:
            continue
        if not crew['desc']:
            crew['desc'] = '[' + str(crew['route'][0]) + ']'
        crew['desc'] = '[]'



    # """
    # Uploading routes to server
    # """
    # for crew in crew_list:
    #     try:
    #         data = {"description": crew['desc'], "properties": {"route": crew['route']}}
    #         r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % crew['iotid'], json = data, headers = headers)
    #         if (r.status_code >= 200) and (r.status_code < 300):
    #             logging.debug("Adding route to crew %d" % crew_list[index])
    #         else:
    #             logging.warning("HTTP Error code while adding route for crew %d" % crew_list[index])
    #     except:
    #             logging.exception("Exception thrown generating route")


"""
Logging data
"""
if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/route.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Router pre-algo started")
    main()
    logging.info("Router pre-algo ended")

    #
    # INPUT_ARRAY = [
    #     {"iotid": 25, "coords": (1, 2)},
    #     {"iotid": 21, "coords": (233, 122)},
    #     {"iotid": 23, "coords": (456, 345)},
    #     {"iotid": 28, "coords": (123, 43)},
    #     {"iotid": 27, "coords": (432, 231)},
    #     {"iotid": 29, "coords": (457, 764)},
    #     {"iotid": 26, "coords": (34, 243)},
    #     {"iotid": 24, "coords": (432, 465)},
    #     {"iotid": 22, "coords": (655, 844)},
    #     {"iotid": 210, "coords": (482, 342)},
    #     {"iotid": 20, "coords": (346, 1234)},
    #     {"iotid": 212, "coords": (431, 678)},
    #     {"iotid": 211, "coords": (835, 46)}
    # ]

    ###############################
    # GA Implementation
    ###############################

    def distance(id_a, id_b):
        a = INPUT_ARRAY[id_a]['coord']
        b = INPUT_ARRAY[id_b]['coord']
        dx = (a[0] - b[0])*110
        dy = (a[1] - b[1])*110
        return math.sqrt(dx*dx + dy*dy)
        # return geopy.distance.distance(a,b).m

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

    # # init to random order
    # def init_distr():
    #     random.seed()
    #     elem = random.choice(init_distr.curr_list)
    #     init_distr.curr_list.remove(elem)
    #     if len(init_distr.curr_list) == 0:
    #         init_distr.curr_list = [i for i in range(0, len(INPUT_ARRAY))]
    #     return elem
    # init_distr.curr_list = [i for i in range(0, len(INPUT_ARRAY))]

    def twoOpt(gene):
        for i in range(len(gene)-1):
            temp_gene = []
            for j in range(0, i):
                temp_gene.append(gene[j])
            temp_gene.append(gene[i+1])
            temp_gene.append(gene[i])
            for j in range(i+2, len(gene)):
                temp_gene.append(gene[j])
            temp_genome = {'path': temp_gene}
            base_genome = {'path': gene}
            if fitness_function(temp_genome) < fitness_function(base_genome):
                gene = copy.deepcopy(temp_gene)
        return gene

    def threeOpt(gene):
        for i in range(len(gene)-2):
            temp_gene = []
            for j in range(0, i):
                temp_gene.append(gene[j])
            temp_gene.append(gene[i+2])
            temp_gene.append(gene[i+1])
            temp_gene.append(gene[i])
            for j in range(i+3, len(gene)):
                temp_gene.append(gene[j])
            temp_genome = {'path': temp_gene}
            base_genome = {'path': gene}
            if fitness_function(temp_genome) < fitness_function(base_genome):
                gene = copy.deepcopy(temp_gene)
        return gene

    def dualOpt(gene):
        gene = copy.deepcopy(twoOpt(gene))
        gene = copy.deepcopy(threeOpt(gene))
        return gene

    def swap(gene):
        # print(gene)
        ind1 = random.randint(0, len(gene)-1)
        ind2 = random.randint(0, len(gene)-1)
        temp = gene[ind2]
        gene[ind2] = gene[ind1]
        gene[ind1] = temp
        return gene

    def mutate(gene):
        x = random.randint(0,100)
        if x < 15:
            gene = copy.deepcopy(scaryShuffle(gene))
        else:
            gene = copy.deepcopy(dualOpt(gene))
        return gene

    def scaryShuffle(gene):
        random.shuffle(gene)
        return gene

    def pmx_randlen(genomes):
        i1 = random.randint(0,len(genomes[0])-1)
        i2 = len(genomes[0])-1 # random.randint(i1+2, len(genomes[0])-1)
        a = genomes[0]
        b = genomes[1]
        # print("Be4a  :" + str(a))
        # print("Be4b  :" + str(b))
        for i in range(i1, i2):
            swap_index = a.index(b[i])
            a[swap_index] = a[i]
            a[i] = b[i]
        # print("After: " + str(a))
        return a

    genome_params = {
        "path": {
            "type": "[int]",
            "size": len(INPUT_ARRAY),
            "possible_values": [i for i in range(len(INPUT_ARRAY))],
            # "initial_distribution": init_distr,
            "mutation_function": mutate,
            "mutation_level": "gene",
            "crossover_function": pmx_randlen,
            "mutation_rate": 1.0
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

    init_pop = []
    starter = [x for x in range(len(INPUT_ARRAY))]
    for i in range(0, 100):
        random.shuffle(starter)
        init_pop.append({"path": copy.deepcopy(starter)})

    final_population = evolver.evolve(
                generation_params={},
                initial_population=init_pop,
                stop_conditions={"target_fitness": 0, "n_generations": 400},
                storage_options={},
                logging_options={})#{'format': '%(message)s', 'level': 20})

    route = []
    # print(fitness_function.best_route_in_history)
    # print([i["iotid"] for i in INPUT_ARRAY])
    for i in fitness_function.best_route_in_history:
        route.append(INPUT_ARRAY[i]['iotid'])

    crew = CREW_ARRAY[0]

    try:
        # print(crew)
        data = {"description": '"' + str(crew['desc']) + '"', "properties": {"route": route}}
        # print(data)
        r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % crew['iotid'], json = data, headers = headers)
        if (r.status_code >= 200) and (r.status_code < 300):
            logging.debug("Adding route to crew")
        else:
            logging.warning(r.status_code)
    except:
            logging.exception("Exception thrown generating route")


    with open("testout.txt", 'a') as fout:
        fout.write(str(dualOpt(fitness_function.best_route_in_history))
                + " :: " + str(fitness_function.best_route_in_history_len) + "\n")
