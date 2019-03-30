import logging
import os
import pickle
import requests
import geopy.distance
import math
import holland 

headers = {"Authorization": "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI="}

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
        bot_list = pickle.load(fin)

    bot_list = [bot for bot in bot_list if bot['status'] != 'Healthy']


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


    for index in bot_list:
        try:
            broken_bot_loc = requests.get(url = "http://routescout.sensorup.com/v1.0/Things("+ str(index['iotid']) + ")/Locations", headers = headers)
            if (broken_bot_loc.status_code >= 200) and (broken_bot_loc.status_code < 300):
                responseJSON = broken_bot_loc.json()
                index['coord'] = responseJSON['value'][0]['location']['coordinates']
            else:
                print("there was an error")
        except:
            logging.exception("Failed getting list of broken bots coordinates")


    """
    Swap coordinate format to [lat,long]
    """
    for crew in crew_list:
        lon, lat = crew['coord'][0], crew['coord'][1]
        crew['coord'] = lat, lon

    for bot in bot_list:
        lon, lat = bot['coord'][0], bot['coord'][1]
        bot['coord'] = lat, lon


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
                for bot in bot_list:
                    if crew_desc[-1] == bot['iotid']:
                        crew['coord'] = bot['coord']
                bot_list = [bot for bot in bot_list if bot['iotid'] not in crew_desc]
            except:
                crew['desc'] = [];


    """
    Specify hyper-parameters for genomes
    """
    broken_bots = {}
    for bot in bot_list:
        broken_bots.update({bot['iotid']: bot['coord']})

    print(broken_bots)

    genome_parameters = {
        "path": {"type": "[int]", "possible_values": broken_bots.keys(), "mutation_function": "swap"}
    }


    """
    Define a fitness function
    A pythonic way to find the length of a round trip
    """
    def distance(p1, p2):
        dist = geopy.distance.distance(p1,p2).m
        return dist

    def sum_of_distances(individual):
        broken_bots = [position[bot] for bot in individual["path"]]
        return sum(
            [distance(bot_1, bot_2) for (bot_1, bot_2) in zip(broken_bots, broken_bots[1:] + [broken_bots[0]])]
        )
    my_population = evolve(
        genome_parameters,
        fitness_function=my_fitness_function,
        anneal_mutation_rate=True,
        show_fitness_plot=True,
        num_generations=100,
    )

    print(my_population)



    """
    Uploading routes to server

    for crew in crew_list:
        try:
            data = {"description": crew['desc'], "properties": {"route": crew['route']}}
            r = requests.patch(url = "http://routescout.sensorup.com/v1.0/Things(%d)" % crew['iotid'], json = data, headers = headers)
            if (r.status_code >= 200) and (r.status_code < 300):
                logging.debug("Adding route to crew %d" % crew_list[index])
            else:
                logging.warning("HTTP Error code while adding route for crew %d" % crew_list[index])
        except:
                logging.exception("Exception thrown generating route")

    """
"""
Logging data
"""
if __name__ == '__main__':
    cwd = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=cwd+'/../../logs/route.log', filemode='a', level=logging.INFO,\
                        format="%(asctime)s [%(levelname)s]: %(message)s")
    logging.info("Router started")
    main()
    logging.info("Router ended")
